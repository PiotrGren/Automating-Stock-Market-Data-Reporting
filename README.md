**Choose your language / Wybierz język**

[EN](#english) / [PL](#polski)

# Automating Stock Market Data Reporting

This repository contains scripts for automating the collection, processing, and reporting of stock market data. The scripts are designed to scrape stock data, process it, and generate reports.

## Repository Structure

├── automat.py

├── company.py

├── Company_Profile.pdf

├── Estimate.xlsx

├── profile.csv

├── REPORT_GENERATOR.py

├── .vscode/

│ └── settings.json

├── FORECAST/

│ └── forecast_AAPL.xlsx

├── WEBSCRAPPING/

│ ├── 25_most_active_stocks.csv

│ ├── 25_most_active_stocks_history.xlsx

│ ├── AAPL.csv

│ ├── scraper.py

│ ├── stocks.csv

│ ├── stocks_history.xlsx

│ ├── tmp_ts.txt

│ └── Sample ML Models/

│ ├── Sample_ML_Model_NN.py

│ ├── Sample_ML_Model_Prophet.py

└── WORKING_SAMPLE_PROJECTS/

├── PROJECT-2.py

├── PROJECT.py

└── readme.txt


## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PiotrGren/Automating-Stock-Market-Data-Reporting.git
   cd Automating-Stock-Market-Data-Reporting
   ```

2. **Install the required packages**:
   Ensure you have `pip` installed. Run the following command to install all necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Scripts Overview

### `automat.py`

This script automates the running of the scraper.py script.

### `company.py`

This script handles the processing of company-specific data - more specifically, the company profile.

### `REPORT_GENERATOR.py`

This script generates PDF reports based on the processed stock market data.

### `WEBSCRAPPING/scraper.py`

This script scrapes stock market data from specified sources (Yahoo Finance).

### `WEBSCRAPPING/Sample ML Models/Sample_ML_Model_NN.py`

This script contains a sample neural network model for predicting stock prices (not fully developed/not working).

### `WEBSCRAPPING/Sample ML Models/Sample_ML_Model_Prophet.py`

This script uses the Prophet library for forecasting stock prices.

## Data Files

- `Company_Profile.pdf`: Sample PDF report generated with `REPORT_GENERATOR.py`.
- `Estimate.xlsx`: Excel file with company earnings and revenue estimate from Yahoo Finance (file is overwritten every time we generate report).
- `profile.csv`: CSV file with company profile such as address, contact etc.(file is overwritten every time we generate report).
- `FORECAST/forecast_AAPL.xlsx`: Excel file with forecasted data for Apple Inc (every time we generate report for specific company new forcast file will be created with company symobl in the name if the forcast\_{ticker_symbol}.xlsx file exists the data will be appended to it).
- `WEBSCRAPPING/25_most_active_stocks.csv`: CSV file with the 25 most active (now).
- `WEBSCRAPPING/25_most_active_stocks_history.xlsx`: Excel file with historical data for the 25 most active stocks.
- `WEBSCRAPPING/AAPL.csv`: CSV file with data for Apple Inc (just a sample file without any application to this project).
- `WEBSCRAPPING/stocks.csv`: CSV file with specific stock data (now).
- `WEBSCRAPPING/stocks_history.xlsx`: Excel file with historical specific stock data (each company has its own sheet called its stock symbol).
- `WEBSCRAPPING/tmp_ts.txt`: Temporary text file for timestamp storage.

## Usage

1. **Scrape Data**:
   Run the `scraper.py` script to scrape stock market data once.

   ```bash
   python WEBSCRAPPING/scraper.py
   ```

   Or run the `automat.py` script to start to start cyclic and automatic scraping of stock market data.

   ```bash
   python automat.py
   ```

2. **Generate Reports**:
   Run the `REPORT_GENERATOR.py` script to generate reports.

   ```bash
   python REPORT_GENERATOR.py [ticker_symbol_here]
   ```

   The script will automatically generate a report for the selected company. The script should be called with the command prompt arguemnt, which should be the ticker symbol of the selected company. Before generating the report, the script also runs the company.py script to gather up-to-date data on the company's profile, events related to the company and estimates on revenue and earnings.

3. **Train and Predict with Machine Learning Models**:
   Check out sample machine-learning models for predicting stock prices (unfinished/broken files).
   **Sample_ML_Model_NN.py** - not working
   **Sample_ML_Model_Prophet.py** - simple working model

## Operation and Data Flow

The main scripts of the project are `REPORT_GENERATOR.py` and `automat.py`. The first one is used to automatically generate stock market reports based on collected data from Yahoo Finance, for a selected company. The second one is used to automatically collect stock market data from Yahoo Finance by using the webscraping mechanism using Python libraries such as Selenium and BeautifulSoup.

### `automat.py`, `WEBSCRAPPING/scraper.py`

The `automat.py` script uses the schedule and subprocess Python libraries to automatically call the `WEBSCRAPPING/scraper.py` script. The process creates a lockfile **lockfile.txt** that tells whether the previous webscraping process has finished. Every 15 seconds, it tries to call a new webscrapping process if the lockfile.txt file has already been deleted (the previous process ended).

The script `WEBSCRAPPING/scraper.py` uses 2 csv files, 2 xlsx files and 1 txt file.

1. **25_most_active_stocks.csv** - stores current data on the 25 most active stock market stocks
2. **stocks.csv** - stores current detailed stock market data of selected companies
3. **tmp_ts.txt** - stores timestamp of current webscrapping
4. **25_most_active_stocks_history.xlsx** - stores historic data on the 25 most active stock market stocks
5. **stoicks_history.xlsx** - stores historic detailed stock market data of selected companies (each company has its own sheet)

#### Operation

First, the script collects information on the 25 most active stock market stocks currently. Then it starts collecting detailed stock market data for each of the 25 companies that will be included in this inventory using the **scrape_stock()** function. Once the scraping is complete, it loads the actual data from the csv files to archive them in xlsx files with the timestamp stored in the tmp_ts.txt file containing the timestamp from the last webscrapping. After archiving, it overwrites the current csv and tmp_ts.txt files with the current data and terminates its operation.

#### Data Flow

```sh
[WEBSCRAPPING_PROCESS]  -->   [LOAD DATA FROM CSV FILES]  -->  [ARCHIVE THEM IN XLSX FILES]  -->  [OVERWRITE CSV FILES AND TIMESTAMP FILE WITH ACTUAL DATA]
```

```sh
stock.csv  --
             | --archiving-data--> stocks_history.xlsx
tmp_ts.txt --
[DATA FROM WEBSCRAPPING] --overwrite--> stocks.csv

25_most_active_stocks.csv --
                            | --archiving-data--> 25_most_active_stocks_history.xlsx
tmp_ts.txt                --
[DATA FROM WEBSCRAPPING] --overwrite--> 25_most_active_stocks.csv

[CURRENT TIME] -- overwrite--> tmp_ts.txt
```

### `REPORT_GENERATOR.py`

#### Operation

This script automatically generates a PDF report for the selected company. It should be called with a command line argument, which should be the ticker symbol of the selected company. This script initially calls the `company.py` script to gather the most up-to-date data on the company's profile and estimates of its revenue and earnings from the Yahoo Finance website. It then generates a report for the selected company using files:

1. **profile.csv** - stores data about company profile (address, contact, industry etc.)
2. **Estimate.xslx** - stores data about company earnings and revenue estimate
3. **stocks.csv** - stores current detailed stock market data of selected companies (script will load data about company we are generating report for)
4. **25_most_active_stocks.csv** - stores current data on the 25 most active stock market stocks (information as an appendix to the report)

Then using **create_pdf()** function and other helper functions, script generates PDF format report using reportlab canva Python library.

Example of running script (for example for Apple Inc.):

```bash
python REPORT_GENERATOR.py AAPL
```

#### Data Flow

```sh
                                                        ---> company.csv
[WEBSCRAPPING COMPANY PROFILE AND EVENTS] --overwrite---|
                                                        ---> Estimate.xlsx
```

```sh
stocks.csv ------------------|
25_most_active_stocks.csv ---|
                             |----------> REPORT_GENERATOR.py/create_pdf() ------> [REPORT IN PDF FORMAT]
company.csv -----------------|
Estimate.xlsx ---------------|
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## Authors

Gabriela Kiwacka - Co-developer - https://github.com/GabrielaKiwacka

Piotr Greń - Co-developer - github.com/PiotrGren
