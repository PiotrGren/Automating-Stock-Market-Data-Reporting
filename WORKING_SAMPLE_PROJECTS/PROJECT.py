'''
import requests
from bs4 import BeautifulSoup

def get_stock_info(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_element = soup.find("span", {"data-reactid": "50"})
    volume_element = soup.find("td", {"data-test": "TD_VOLUME-value"})
    market_cap_element = soup.find("td", {"data-test": "MARKET_CAP-value"})
    high_element = soup.find("td", {"data-test": "FIFTY_TWO_WK_HIGH-value"})
    low_element = soup.find("td", {"data-test": "FIFTY_TWO_WK_LOW-value"})
    change_percent_element = soup.find("span", {"data-reactid": "51"})

    price = price_element.text if price_element else "N/A"
    volume = volume_element.text if volume_element else "N/A"
    market_cap = market_cap_element.text if market_cap_element else "N/A"
    high = high_element.text if high_element else "N/A"
    low = low_element.text if low_element else "N/A"
    change_percent = change_percent_element.text if change_percent_element else "N/A"

    return {
        "Price": price,
        "Volume": volume,
        "Market Cap": market_cap,
        "52 Week High": high,
        "52 Week Low": low,
        "Change Percent": change_percent
    }

# Przykładowe użycie
symbol = "TSLA"  # Symbol akcji firmy, np. "AAPL" dla Apple Inc.
stock_info = get_stock_info(symbol)
for key, value in stock_info.items():
    print(f"{key}: {value}")
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium.common.exceptions import WebDriverException
import time


def get_stock_data(symbol, days_back):
    # Utwórz nową instancję przeglądarki Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uruchom w trybie bezgłowiczym (bez okna przeglądarki)
    service = Service('C:/Program Files/ChromeDriver/chromedriver.exe')  # Podaj ścieżkę do chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Pobierz dane z Yahoo Finance
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    url = f"https://finance.yahoo.com/quote/{symbol}/history?period1={start_date}&period2={end_date}&interval=1d"
    driver.get(url)
    time.sleep(10)  # Poczekaj, aż strona się załaduje (zmieniamy czas oczekiwania na 10 sekund)

    # Znajdź tabelę z danymi
    try:
        table = driver.find_element(By.XPATH, "//table[@data-test='historical-prices']")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Zapisz dane do słownika
        stock_data = []
        for row in rows[1:]:  # Pomiń pierwszy wiersz, ponieważ to nagłówki
            cells = row.find_elements(By.TAG_NAME, "td")
            date = cells[0].text
            open_price = cells[1].text
            high_price = cells[2].text
            low_price = cells[3].text
            close_price = cells[4].text
            volume = cells[6].text
            stock_data.append({
                "Date": date,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Close": close_price,
                "Volume": volume
            })
    except WebDriverException:
        print("Nie można znaleźć tabeli z danymi historycznymi")
        stock_data = None

    # Zamknij przeglądarkę
    driver.quit()

    return stock_data

# Przykładowe użycie
symbol = "AAPL"  # Symbol akcji firmy, np. "AAPL" dla Apple Inc.
days_back = 3  # Ilość dni wstecz, dla których chcemy pobrać dane

stock_data = get_stock_data(symbol, days_back)
for data in stock_data:
    print(data)

