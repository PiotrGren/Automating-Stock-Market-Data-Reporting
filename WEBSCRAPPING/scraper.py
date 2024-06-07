from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException, NoSuchElementException
import sys
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_stock(driver, ticker_symbol):
    # build the URL of the target page
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}'

    # visit the target page
    driver.get(url)

    #wait = WebDriverWait(driver, 20)
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[class="btn secondary accept-all"][name="agree"][value="agree"]'))).click()

    try:
        # wait up to 3 seconds for the consent modal to show up
        consent_overlay = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.consent-overlay')))

        # click the 'Accept all' button
        accept_all_button = consent_overlay.find_element(By.CSS_SELECTOR, '.accept-all')
        accept_all_button.click()
    except TimeoutException:
        pass

    # initialize the dictionary that will contain
    # the data collected from the target page
    stock = { 'Symbol': ticker_symbol }
#f'[data-symbol="{ticker_symbol}"][data-field="preMarketPrice"]') \
    try:
    # Sprawdź, czy istnieje element pre-market price
        regular_market_price = driver \
            .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="preMarketPrice"]') \
            .text
        regular_market_change = driver \
            .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="preMarketChange"]') \
            .text
        regular_market_change_percent = driver \
            .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="preMarketChangePercent"]') \
            .text \
            .replace('(', '').replace(')', '') 
    except NoSuchElementException:
    # scraping the stock data from the price indicators
        try:
            regular_market_price = driver \
                .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPrice"]') \
                .text
            regular_market_change = driver \
                .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChange"]') \
                .text
            regular_market_change_percent = driver \
                .find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketChangePercent"]') \
                .text \
                .replace('(', '').replace(')', '')
        except NoSuchElementException:
            return None

    stock['regular_market_price'] = regular_market_price
    stock['regular_market_change'] = regular_market_change
    stock['regular_market_change_percent'] = regular_market_change_percent
    #stock['pre_market_price'] = pre_market_price
    #stock['pre_market_change'] = pre_market_change
    #stock['pre_market_change_percent'] = pre_market_change_percent

    
    previous_close = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    open_value = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketOpen"]').text
    #bid = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    #ask = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    #days_range = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    #week_range = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    volume = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketVolume"]').text
    avg_volume = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="averageVolume"]').text
    market_cap = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="marketCap"]').text
    beta = driver.find_element(By.CSS_SELECTOR, f'[class = "value svelte-tx3nkj"]').text
    pe_ratio = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="trailingPE"]').text
    eps = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="trailingPE"]').text
    #earnings_date = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    #dividend_yield = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    #ex_dividend_date = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="regularMarketPreviousClose"]').text
    year_target_est = driver.find_element(By.CSS_SELECTOR, f'[data-symbol="{ticker_symbol}"][data-field="targetMeanPrice"]').text

    stock['previous_close'] = previous_close
    stock['open_value'] = open_value
    #stock['bid'] = bid
    #stock['ask'] = ask
    #stock['days_range'] = days_range
    #stock['week_range'] = week_range
    stock['volume'] = volume
    stock['avg_volume'] = avg_volume
    stock['market_cap'] = market_cap
    stock['beta'] = beta
    stock['pe_ratio'] = pe_ratio
    stock['eps'] = eps
    #stock['earnings_date'] = earnings_date
    #stock['dividend_yield'] = dividend_yield
    #stock['ex_dividend_date'] = ex_dividend_date
    stock['year_target_est'] = year_target_est
    
    # scraping the stock data from the "Summary" table

    return stock

url = 'https://finance.yahoo.com/most-active/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

timestamp = datetime.now().strftime('%d-%m-%Y %H:%M')

table = soup.find('table')
table_rows = table.find_all('tr')
th = table.find_all('th')
names = [i.text for i in th]
fortune = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    fortune.append(row)

fortune = pd.DataFrame(fortune, columns = names)
fortune.drop(0, axis = 0, inplace = True)
fortune.drop(fortune.columns[-1], axis = 1, inplace=True)
fortune


#SZCZEGÓŁOWE DANE
'''
if len(sys.argv) <= 1:
    print('Ticker symbol CLI argument missing!')
    sys.exit(2)
'''
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
driver.set_window_size(1150, 1000)

stocks = []
'''
for ticker_symbol in sys.argv[1:]:
    stocks.append(scrape_stock(driver, ticker_symbol))
'''
for tricker_symbol in fortune['Symbol']:
    returned = scrape_stock(driver, tricker_symbol)
    if returned is None:
        continue
    else:
        stocks.append(returned)

AAPL = "AAPL"
if AAPL in fortune["Symbol"].values:
    pass
else:
    returned = scrape_stock(driver, AAPL)
    if returned is None:
        pass
    else:
        stocks.append(returned)


driver.quit()


######################################################################################

# Archiwizacja danych

# Funkcja do odczytu pliku CSV
def read_csv(filename):
    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
            return data
    except FileNotFoundError:
        return []

# Odczyt timestampu z pliku tmp_ts.txt
with open('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/tmp_ts.txt', 'r') as file:
    timestamp_history = file.read()

# Odczytanie danych z plików CSV
fortune_data = pd.read_csv('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/25_most_active_stocks.csv')
stocks_data = pd.read_csv('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/stocks.csv')

fortune_data.head()
stocks_data.head()

# Zapis do plików historii
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def append_to_history(filename, data, timestamp):
    with pd.ExcelWriter(filename, mode="a", engine="openpyxl") as writer:
        # Sprawdź istniejące arkusze w pliku Excel
        try:
            with pd.ExcelFile(filename) as xls:
                existing_sheets = xls.sheet_names
        except FileNotFoundError:
            existing_sheets = []

    for index, row in data.iterrows():
        symbol = row["Symbol"]
        sheet_name = symbol

        if sheet_name in existing_sheets:
            '''
            with pd.ExcelWriter(filename, mode="a", engine="openpyxl", if_sheet_exists="error") as writer_existing:
                data_to_append = pd.DataFrame(row).transpose()
                data_to_append["Timestamp"] = timestamp
                data_to_append.to_excel(writer_existing, index=False, sheet_name=sheet_name, header=False)
            '''
            workbook = load_workbook(filename)
            worksheet = workbook[sheet_name]
            data_to_append = pd.DataFrame(row).transpose()
            data_to_append["Date"] = timestamp.split(' ')[0]
            data_to_append["Time"] = timestamp.split(' ')[1]
            for row in dataframe_to_rows(data_to_append, index = False, header = False):
                worksheet.append(row)
            workbook.save(filename)
            workbook.close()
        else:
             # Jeśli arkusz nie istnieje, stwórz nowy arkusz i dopisz dane
            with pd.ExcelWriter(filename, mode="a", engine="openpyxl") as writer_new:
                data_to_append = pd.DataFrame(row).transpose()
                data_to_append["Date"] = timestamp.split(' ')[0]
                data_to_append["Time"] = timestamp.split(' ')[1]
                data_to_append.to_excel(writer_new, index=False, sheet_name=sheet_name)

# Dodanie danych do plików historii
append_to_history('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/25_most_active_stocks_history.xlsx', fortune_data, timestamp_history)
append_to_history('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/stocks_history.xlsx', stocks_data, timestamp_history)


fortune.to_csv('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/25_most_active_stocks.csv', index=False)

csv_header = stocks[0].keys()
with open('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/stocks.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, csv_header)
    dict_writer.writeheader()
    dict_writer.writerows(stocks)

    
with open('C:/Users/Piotrek/Desktop/Uczelnia/III rok/Semestr II/Usługi Sieciowe w Biznesie/Projekt/WEBSCRAPPING/tmp_ts.txt', 'w') as file:
    file.write(timestamp)