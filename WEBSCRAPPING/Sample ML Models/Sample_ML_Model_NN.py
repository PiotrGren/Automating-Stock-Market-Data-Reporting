import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import load_model
import openpyxl
from sklearn.model_selection import train_test_split

# Wczytaj dane z pliku CSV (AAPL.csv)
aapl_data = pd.read_csv("C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/AAPL.csv")

# Konwertuj kolumnę 'Date' na datetime
aapl_data['Date'] = pd.to_datetime(aapl_data['Date'])

# Wybierz kolumny potrzebne do trenowania modelu
aapl_data = aapl_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Ustaw datę jako indeks
aapl_data.set_index('Date', inplace=True)

# Normalizuj dane
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(aapl_data)

# Tworzenie zbioru treningowego i testowego
train_data_len = int(len(scaled_data) * 0.7)
train_data = scaled_data[:train_data_len]
test_data = scaled_data[train_data_len:]

# Tworzenie zbioru treningowego
x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i])
    y_train.append(train_data[i, 3])  # Cena zamknięcia

x_train, y_train = np.array(x_train), np.array(y_train)

# Budowa modelu LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=25))
model.add(Dense(units=1))

# Kompilacja modelu
model.compile(optimizer='adam', loss='mean_squared_error')

# Trenowanie modelu na danych z AAPL.csv
model.fit(x_train, y_train, batch_size=1, epochs=1)

# Zapisanie modelu po wstępnym trenowaniu
model.save('stock_model_initial.h5')

# Wczytanie danych z pliku Excel (stock_history.xlsx)
excel_data = pd.ExcelFile('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/stocks_history.xlsx')


# Przechodzenie przez każdy arkusz w pliku Excel
for sheet in excel_data.sheet_names:
    df = pd.read_excel(excel_data, sheet_name=sheet)
    
    # Usuń pierwszą kolumnę
    df = df.drop(columns="Symbol")
    
    #df['regular_market_price'] = df['regular_market_price'].str.replace(',', '.').astype(float)
    #df['regular_market_change'] = df['regular_market_change'].str.replace(',', '.').astype(float)
    #df['previous_close'] = df['previous_close'].str.replace(',', '.').astype(float)
    #df['open_value'] = df['open_value'].str.replace(',', '.').astype(float)
    #df['beta'] = df['beta'].str.replace(',', '.').astype(float)
    #df['pe_ratio'] = df['pe_ratio'].str.replace(',', '.').astype(float)
    #df['year_target_est'] = df['year_target_est'].str.replace(',', '.').astype(float)
    #df['eps'] = df['eps'].str.replace(',', '.').astype(float)

    # Zamień kolumnę 'regular_market_change_percent' na liczbę
    df['regular_market_change_percent'] = df['regular_market_change_percent'].str.replace('%', '')
    
    # Usuń znaki %, + z przodu liczb dodatnich oraz zamień znaki - na liczby ujemne
    df['regular_market_change_percent'] = df['regular_market_change_percent'].str.replace('+', '')
    df['regular_market_change_percent'] = df['regular_market_change_percent'].str.replace('-', '-').astype(float)
    
    # Usuń przecinki z kolumn 'volume' oraz 'avg_volume'
    df['volume'] = df['volume'].str.replace(',', '').astype(int)
    df['avg_volume'] = df['avg_volume'].str.replace(',', '').astype(int)
    
    # Usuń literę T z kolumny 'market_cap' i przekonwertuj wartości na liczby
    df['market_cap'] = df['market_cap'].str.replace('T', '')
    df['market_cap'] = df['market_cap'].str.replace('B', '')
    df['market_cap'] = df['market_cap'].str.replace(',', '.').astype(float)
    
    # Upewnij się, że data jest posortowana rosnąco
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), dayfirst=True)
    
    # Normalizacja danych
    df.set_index('Datetime', inplace=True)
    df_scaled = scaler.fit_transform(df)
    
    # Tworzenie zbioru treningowego
    X = df.drop(columns='regular_market_price')
    y = df['regular_market_price']

    X_train, y_train, X_test, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
    
    # Dostrajanie modelu na danych z aktualnego arkusza
    model.fit(X_train, y_train, batch_size=1, epochs=1, verbose=1)

print("KONIEC")
model.save('stock_model_final.h5')

# Przewidywanie przyszłych cen akcji
def predict_future_prices(model, data, days):
    predictions = []
    current_data = data[-60:]

    for _ in range(days):
        current_data = np.reshape(current_data, (1, current_data.shape[0], current_data.shape[1]))
        predicted_price = model.predict(current_data)
        predictions.append(predicted_price[0, 0])
        new_data = np.append(current_data[0, 1:], predicted_price, axis=0)
        current_data = new_data

    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# Przewidywanie ceny akcji na 30 dni do przodu
predicted_prices = predict_future_prices(model, scaled_data, 30)

# Przekształcenie przewidywanych cen z powrotem do oryginalnej skali
predicted_prices = scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))

# Generowanie dat dla przyszłych przewidywań
last_date = aapl_data.index[-1]
future_dates = pd.date_range(last_date, periods=31, closed='right')

# Wyświetlanie przewidywanych cen i dat
for date, price in zip(future_dates, predicted_prices):
    print(f"Date: {date}, Predicted Price: {price[0]}")
