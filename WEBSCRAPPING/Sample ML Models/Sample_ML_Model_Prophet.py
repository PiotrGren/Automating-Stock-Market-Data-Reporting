import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
import numpy as np
import pandas as pd

#data = pd.read_csv("C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/AAPL.csv")

data = yf.download('AAPL', start='2021-01-01')

data

data_close = data[['Close']]
data_close.reset_index(inplace=True)
data_close.columns = ['ds', 'y']
data_close.loc[:, 'MA'] = data_close['y'].rolling(window=80).mean().fillna(0)

data_close.loc[:, 'Indicator'] = np.where(data_close['y'] > data_close['MA'], 'Buy', 'Sell')

def score_func(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)

tscv = TimeSeriesSplit(n_splits=5)
scores = []

for train_index, test_index in tscv.split(data_close):
    
    train_data = data_close.iloc[train_index]
    test_data = data_close.iloc[test_index]
    
    m = Prophet(yearly_seasonality=True)
    m.fit(train_data)
    
    future = m.make_future_dataframe(periods=len(test_data))
    forecast = m.predict(future)
    test_predictions = forecast.iloc[-len(test_data):][['yhat']]
   
    score = score_func(test_data[['y']], test_predictions)
    
    scores.append(score)

mean_score = sum(scores) / len(scores)

m = Prophet(yearly_seasonality=True)
m.fit(data_close)

future = m.make_future_dataframe(periods=365 * 2)
forecast = m.predict(future)

forecast['MA'] = forecast['yhat'].rolling(window=80).mean().fillna(0)
forecast['Indicator'] = np.where(forecast['yhat'] < forecast['MA'], 'Buy', 'Sell')

forecast.head()


plt.figure(figsize=(15, 8))
fig1 = m.plot(forecast)
#plt.scatter(forecast['ds'], forecast['yhat'], c=np.where(forecast['Indicator'] == 'Buy', 'green', 'red'), label='Indicator')
#buy_signals = forecast[forecast['Indicator'] == 'Buy']
#sell_signals = forecast[forecast['Indicator'] == 'Sell']

#plt.scatter(buy_signals['ds'], buy_signals['yhat'], color='green', marker='^', label='Buy')
#plt.scatter(sell_signals['ds'], sell_signals['yhat'], color='red', marker='v', label='Sell')

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Stock Price')

plt.grid(True)

print("Cross Validation Score : ", mean_score)

plt.show()