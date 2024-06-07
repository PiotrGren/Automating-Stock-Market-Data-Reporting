from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException, NoSuchElementException
from openpyxl import Workbook
import sys
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_profile(driver, ticker_symbol):
    # build the URL of the target page
    url = f'https://finance.yahoo.com/quote/{ticker_symbol}/profile'

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
    co_name = driver \
        .find_element(By.CSS_SELECTOR, '[class="svelte-3a2v0c"]').text
    profile = {'CO_Name': co_name}

    address = driver.find_element(By.CSS_SELECTOR, '[class="address svelte-wxp4ja"]').text
    location = address.split("\n")[0]
    city = address.split("\n")[1]
    country = address.split("\n")[2]
    profile['Location'] = location
    profile['City'] = city
    profile['Country'] = country

    co_stats = driver.find_element(By.CSS_SELECTOR, '[class="company-stats svelte-wxp4ja"]').text
    sector = co_stats.split("\n")[1]
    industry = co_stats.split("\n")[3]
    fte = co_stats.split("\n")[5]
    profile['Sector'] = sector
    profile["Industry"] = industry
    profile["Full Time Employees"] = fte

    phone_number = driver.find_element(By.CSS_SELECTOR, '[aria-label="phone number"][data-v9y="1"]').text
    website = driver.find_element(By.CSS_SELECTOR, '[aria-label="website link"][data-v9y="1"]').text
    profile["Phone Number"] = phone_number
    profile["Website"] = website

    for i in range(3):
        try:
            ue = driver.find_element(By.XPATH, f'//section[@data-testid="upcoming-events"]/div[{i+1}]').text
        except NoSuchElementException:
            break
        if i == 0:
            upcoming = ue
        else:
            upcoming = upcoming + "NEW" + ue
    profile["UpcomingEvents"] = upcoming

    for i in range(3):
        try:
            re = driver.find_element(By.XPATH, f'//section[@data-testid="recent-events"]/ul/li[{i+1}]').text
        except NoSuchElementException:
            try:
                re = driver.find_element(By.XPATH, f'//section[@data-testid="recent-events"]/div/div[{i+1}]').text
            except NoSuchElementException:
                break
        if i == 0:
            recent = re
        else:
            recent = recent + 'NEW' + re
    profile["RecentEvents"] = recent

    url = f"https://finance.yahoo.com/quote/{ticker_symbol}/analysis"
    driver.get(url)

    col1 = []
    col1.append(driver.find_element(By.XPATH, '//section[@data-testid="earningsEstimate"]/div[@class="tableContainer svelte-17yshpm"]/table[@class="svelte-17yshpm"]/thead/tr/th').text)
    for i in range(4):
        col1.append(driver.find_element(By.XPATH, f'//section[@data-testid="earningsEstimate"]/div[@class="tableContainer svelte-17yshpm"]/table[@class="svelte-17yshpm"]/tbody/tr[{i+1}]/td').text)

    col2 = []
    col2.append(driver.find_element(By.XPATH, '//section[@data-testid="earningsEstimate"]/header/h3').text)
    for i in range(4):
        col2.append(driver.find_element(By.XPATH, f'//section[@data-testid="earningsEstimate"]/div[@class="tableContainer svelte-17yshpm"]/table[@class="svelte-17yshpm"]/tbody/tr[{i+1}]/td[3]').text)

    col3 = []
    col3.append(driver.find_element(By.XPATH, '//section[@data-testid="revenueEstimate"]/header/h3').text)
    for i in range(4):
        col3.append(driver.find_element(By.XPATH, f'//section[@data-testid="revenueEstimate"]/div[@class="tableContainer svelte-17yshpm"]/table[@class="svelte-17yshpm"]/tbody/tr[{i+1}]/td[3]').text)


    print(col1)
    print(col2)
    print(col3)
    estimate = pd.DataFrame({
        col1[0]: col1[1:],
        col2[0]: col2[1:],
        col3[0]: col3[1:]
    })  
    estimate_name = driver.find_element(By.XPATH, '//section[@data-testid="earningsEstimate"]/div[@class="tableContainer svelte-17yshpm"]/table[@class="svelte-17yshpm"]/thead/tr/th[3]').text
    '''
    dataframes = []
    rows = tables.find_element(By.TAG_NAME, 'tr')
    data = []
    for row in rows:
        cols = row.find_element(By.TAG_NAME, 'td')
        cols = [col.text for col in cols]
        data.append(cols)
    df = pd.DataFrame(data[1:], coumns = data[0])
    dataframes.append(df)

    df.head()
    '''
    
    
    return profile, estimate, estimate_name

if len(sys.argv) <= 1:
    print('Ticker symbol CLI argument missing!')
    sys.exit(2)
else:
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.set_window_size(1150, 1000)

    profile = []
    toappend, estimate, name = scrape_profile(driver, sys.argv[1])
    profile.append(toappend)

    driver.quit()

    wb = Workbook()
    wb.save("Estimate.xlsx")

    estimate.to_excel('Estimate.xlsx', index=False, sheet_name=name)

    with open('profile.csv', 'w', newline='') as csvfile:
        fieldnames = profile[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in profile:
            writer.writerow(entry)