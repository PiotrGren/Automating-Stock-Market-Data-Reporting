**Choose your language / Wybierz język**

[EN](#english) / [PL](#polski)

## Repository Structure / Struktura repozytorium

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

#### English

# Automating Stock Market Data Reporting

## Table of Contents

1. [Description](#description)
2. [Setup](#setup)
3. [Script Overview](#script-overview)
4. [Data Files](#data-files)
5. [Usage](#usage)
6. [Operation and Data Flow](#operation-and-data-flow)
7. [Report Structure](#report-structure)
8. [License](#license)
9. [Contributing](#contributing)
10. [Authors](#authors)

## Description

This repository contains scripts for automating the collection, processing, and reporting of stock market data. The scripts are designed to scrape stock data, process it, and generate reports in PDF format.

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

## Report Structure

The report consists of 4 pages.

#### Page 1

On the first page you will find information on the company's profile, the company's upcoming events, the company's recent events, and the company's revenue and earnings estimates for the next quarter. The page uses **profile.csv** and **Estimate.xlsx** files to generate its content.

#### Page 2
On the second page is a chart of stock prices for the last day (currently for the last lines because the data was collected irregularly, the script should be improved if someone decides to collect this data continuously and very regularly). This chart is generated from the data in the **stocks_history.xlsx** file and shows stock prices over time. Underneath the chart is the company's current detailed stock market data, which is taken from the **stocks.csv** file.

#### Page 3
On page 3 is a chart of stock prices over the past year. The time series is matched with a **Prophet** machine learning model that predicts prices for the next week. To learn more check out the **history_chart()** function in the `REPORT_GENERATOR.py` file. The chart also shows the largest and smallest closing price of the last year. as well as the last closing price. Underneath the chart are the stock price value predictions for the next week, along with a 'Buy' or 'Sell' indicator. This indicator is calculated based on a moving average.

#### Page 4
On the fourth page, as additional information, there is a table of the 25 most active stock market stocks currently. This table is downloaded and generated from the **@5_most_active_stocks.csv** file.

## License

This project is licensed under the MIT License. See the LICENSE.txt file for details.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## Authors

Gabriela Kiwacka - Co-developer - https://github.com/GabrielaKiwacka

Piotr Greń - Co-developer - github.com/PiotrGren



#### Polski

# Automatyzacja Raportowania Danych Giełdowych

## Spis treści

1. [Opis](#opis)
2. [Instalacja](#instalacja)
3. [Przegląd Skryptów](#przegląd-skryptów)
4. [Pliki Danych](#pliki-danych)
5. [Wykorzystanie](#wykorzystanie)
6. [Działanie i Przepływ Danych](#działanie-i-przepływ-danych)
7. [Struktura Raportu](#struktura-raportu)
8. [Licencja](#licencja)
9. [Wkład](#wkład)
10. [Autorzy](#autorzy)

## Opis

To repozytorium zawiera skrypty do automatyzacji gromadzenia, przetwarzania i raportowania danych giełdowych. Skrypty są przeznaczone do pobierania danych giełdowych, przetwarzania ich i generowania raportów w formacie PDF.

## Instalacja

1. **Sklonuj repozytorium**:

   ```bash
   git clone https://github.com/PiotrGren/Automating-Stock-Market-Data-Reporting.git
   cd Automating-Stock-Market-Data-Reporting
   ```

2. **Zainstaluj wymagane pakiety**:
   Ensure you have `pip` installed. Run the following command to install all necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Przegląd Skryptów

### `automat.py`

Ten skrypt automatyzuje uruchamianie skryptu scraper.py.

### `company.py`

Ten skrypt obsługuje przetwarzanie danych specyficznych dla firmy - a dokładniej profilu firmy.

### `REPORT_GENERATOR.py`

Skrypt ten generuje raporty PDF na podstawie przetworzonych danych giełdowych.

### `WEBSCRAPPING/scraper.py`

Skrypt ten pobiera dane giełdowe z Yahoo Finance.

### `WEBSCRAPPING/Sample ML Models/Sample_ML_Model_NN.py`

Ten skrypt zawiera przykładowy model sieci neuronowej do przewidywania cen akcji (nie jest w pełni rozwinięty/nie działa).

### `WEBSCRAPPING/Sample ML Models/Sample_ML_Model_Prophet.py`

Skrypt ten wykorzystuje bibliotekę Prophet do prognozowania cen akcji.

## Pliki Danych

- `Company_Profile.pdf`: Przykładowy raport PDF wygenerowany za pomocą `REPORT_GENERATOR.py`.
- `Estimate.xlsx`: Plik Excel z szacunkami zysków i przychodów firmy z Yahoo Finance (plik jest nadpisywany za każdym razem, gdy generujemy raport).
- `profile.csv`: Plik CSV z profilem firmy, takim jak adres, kontakt itp. (plik jest nadpisywany za każdym razem, gdy generujemy raport).
- `FORECAST/forecast_AAPL.xlsx`: Plik Excel z prognozowanymi danymi dla Apple Inc (za każdym razem, gdy generujemy raport dla konkretnej firmy, zostanie utworzony nowy plik forcast z symbolem firmy w nazwie, jeśli plik forcast\_{ticker_symbol}.xlsx istnieje, dane zostaną do niego dołączone).
- `WEBSCRAPPING/25_most_active_stocks.csv`: Plik CSV z 25 najbardziej aktywnymi (obecnie) akcjami.
- `WEBSCRAPPING/25_most_active_stocks_history.xlsx`: Plik Excel z danymi historycznymi dla 25 najbardziej aktywnych akcji.
- `WEBSCRAPPING/AAPL.csv`: Plik CSV z danymi dla Apple Inc (tylko przykładowy plik bez żadnego zastosowania w tym projekcie).
- `WEBSCRAPPING/stocks.csv`: Plik CSV z konkretnymi danymi giełdowymi (obecnie).
- `WEBSCRAPPING/stocks_history.xlsx`: Plik Excel z historycznymi danymi akcji (każda spółka ma własny arkusz o nazwie symbolu akcji).
- `WEBSCRAPPING/tmp_ts.txt`: Tymczasowy plik tekstowy do przechowywania znaczników czasu.

## Wykorzystanie

1. **Zbieranie danych**:
   Uruchom skrypt `WEBSCRAPPING/scraper.py`, aby jednorazowo zebrać dane giełdowe.

   ```bash
   python WEBSCRAPPING/scraper.py
   ```

   Lub uruchom skrypt `automat.py`, aby rozpocząć cykliczne i automatyczne pobieranie danych giełdowych.

   ``bash
   python automat.py
   ```

2. **Generowanie raportów**:
   Uruchom skrypt `REPORT_GENERATOR.py`, aby wygenerować raporty.

   ```bash
   python REPORT_GENERATOR.py [ticker_symbol_here]
   ```

   Skrypt automatycznie wygeneruje raport dla wybranej spółki. Skrypt należy wywołać z argumentem wiersza poleceń, którym powinien być symbol giełdowy wybranej spółki. Przed wygenerowaniem raportu skrypt uruchamia również skrypt company.py w celu zebrania aktualnych danych na temat profilu spółki, wydarzeń z nią związanych oraz szacunkowych przychodów i zysków.

3. **Trenowanie i przewidywanie cen akcji modelami nauczania maszynowego**:
   Sprawdź przykładowe modele uczenia maszynowego do przewidywania cen akcji (pliki niedokończone/robocze).
   **Sample_ML_Model_NN.py** - nie działa
   **Sample_ML_Model_Prophet.py** - prosty działający model

## Działanie i Przepływ Danych

Głównymi skryptami projektu są `REPORT_GENERATOR.py` i `automat.py`. Pierwszy z nich służy do automatycznego generowania raportów giełdowych na podstawie zebranych danych z Yahoo Finance dla wybranej spółki. Drugi służy do automatycznego zbierania danych giełdowych z Yahoo Finance za pomocą mechanizmu webscrapingu przy użyciu bibliotek Pythona, takich jak Selenium i BeautifulSoup.

### `automat.py`, `WEBSCRAPPING/scraper.py`

Skrypt `automat.py` używa bibliotek schedule i subprocess Pythona do automatycznego wywoływania skryptu `WEBSCRAPPING/scraper.py`. Proces tworzy plik blokady **lockfile.txt**, który informuje, czy poprzedni proces webscrapingu został zakończony. Co 15 sekund próbuje wywołać nowy proces webscrappingu, jeśli plik lockfile.txt został już usunięty (poprzedni proces zakończył się).

Skrypt `WEBSCRAPPING/scraper.py` używa 2 plików csv, 2 plików xlsx i 1 pliku txt.

1. **25_most_active_stocks.csv** - przechowuje aktualne dane na temat 25 najbardziej aktywnych akcji giełdowych
2. **stocks.csv** - przechowuje aktualne szczegółowe dane giełdowe wybranych spółek
3. **tmp_ts.txt** - przechowuje znacznik czasu bieżącego webscrappingu
4. **25_most_active_stocks_history.xlsx** - przechowuje historyczne dane na temat 25 najbardziej aktywnych akcji giełdowych.
5. **stoicks_history.xlsx** - przechowuje historyczne szczegółowe dane giełdowe wybranych spółek (każda spółka ma swój własny arkusz)

#### Działanie

Najpierw skrypt zbiera informacje o 25 najbardziej aktywnych obecnie akcjach giełdowych. Następnie rozpoczyna zbieranie szczegółowych danych giełdowych dla każdej z 25 spółek, które zostaną uwzględnione w tym wykazie za pomocą funkcji **scrape_stock()**. Po zakończeniu skrobania ładuje rzeczywiste dane z plików csv, aby zarchiwizować je w plikach xlsx ze znacznikiem czasu przechowywanym w pliku tmp_ts.txt zawierającym znacznik czasu z ostatniego skrobania. Po zarchiwizowaniu nadpisuje bieżące pliki csv i tmp_ts.txt aktualnymi danymi i kończy działanie.

#### Przepływ Danych

```sh
[PROCES WEBSCRAPPINGU]  -->   [ZAŁADOWANIE DANYCH Z PLIKÓ CSV]  -->  [ARCHIWIZACJA DANYCH W PLIKACH XLSX]  -->  [NADPISANIE PLIKÓW CSV ORAZ TIMESTAMP AKTUALNYMI DANYMI]
```

```sh
stock.csv  --
             | --archiwizacja-danych--> stocks_history.xlsx
tmp_ts.txt --


[DATA FROM WEBSCRAPPING] --nadpisanie--> stocks.csv

25_most_active_stocks.csv --
                            | --archiwizacja-danych--> 25_most_active_stocks_history.xlsx
tmp_ts.txt                --


[DATA FROM WEBSCRAPPING] --nadpisanie--> 25_most_active_stocks.csv

[CURRENT TIME] -- nadpisanie--> tmp_ts.txt
```

### `REPORT_GENERATOR.py`

#### Działanie

Ten skrypt automatycznie generuje raport PDF dla wybranej spółki. Należy go wywołać z argumentem wiersza poleceń, którym powinien być symbol giełdowy wybranej spółki. Skrypt ten początkowo wywołuje skrypt `company.py` w celu zebrania najbardziej aktualnych danych na temat profilu firmy oraz szacunków jej przychodów i zysków ze strony internetowej Yahoo Finance. Następnie generuje raport dla wybranej spółki przy użyciu plików:

1. **profile.csv** - przechowuje dane o profilu firmy (adres, kontakt, branża itp.)
2. **Estimate.xslx** - przechowuje dane o szacunkowych zyskach i przychodach firmy
3. **stocks.csv** - przechowuje aktualne szczegółowe dane giełdowe wybranych spółek (skrypt załaduje dane o spółce, dla której generujemy raport)
4. **25_most_active_stocks.csv** - przechowuje aktualne dane o 25 najbardziej aktywnych akcjach giełdowych (informacja jako załącznik do raportu).

Następnie przy użyciu funkcji **create_pdf()** i innych funkcji pomocniczych, skrypt generuje raport w formacie PDF przy użyciu biblioteki reportlab canva Python.

Przykład uruchomionego skryptu (na przykład dla Apple Inc.):
```bash
python REPORT_GENERATOR.py AAPL
```

#### Data Flow

```sh
                                                           ---> company.csv
[WEBBSCRAPING PROFILU FIRMY I JEJ WYDARZEŃ] --overwrite---|
                                                           ---> Estimate.xlsx
```

```sh
stocks.csv ------------------|
25_most_active_stocks.csv ---|
                             |----------> REPORT_GENERATOR.py/create_pdf() ------> [RAPORT W FORMACIE PDF]
company.csv -----------------|
Estimate.xlsx ---------------|
```

## Struktura Raportu

Raport składa się z 4 stron.

#### Strona 1

Na pierwszej stronie znajdują się informacje o profilu firmy, nadchodzących wydarzeniach, ostatnich wydarzeniach oraz szacunkach przychodów i zysków firmy na następny kwartał. Strona wykorzystuje pliki **profile.csv** i **Estimate.xlsx** do wygenerowania swojej zawartości.

#### Strona 2
Na drugiej stronie znajduje się wykres cen akcji za ostatni dzień (obecnie za ostatnie wiersze, ponieważ dane były zbierane nieregularnie, skrypt powinien zostać ulepszony, jeśli ktoś zdecyduje się zbierać te dane w sposób ciągły i bardzo regularny). Ten wykres jest generowany na podstawie danych z pliku **stocks_history.xlsx** i pokazuje ceny akcji w czasie. Pod wykresem znajdują się aktualne szczegółowe dane giełdowe spółki, które są pobierane z pliku **stocks.csv**.

#### Strona 3
Na stronie 3 znajduje się wykres cen akcji w ciągu ostatniego roku. Szereg czasowy jest dopasowany do modelu uczenia maszynowego **Prophet**, który przewiduje ceny na następny tydzień. Aby dowiedzieć się więcej, sprawdź funkcję **history_chart()** w pliku `REPORT_GENERATOR.py`. Wykres pokazuje również największą i najmniejszą cenę zamknięcia z ostatniego roku, a także ostatnią cenę zamknięcia. Pod wykresem znajdują się prognozy cen akcji na następny tydzień wraz ze wskaźnikiem „Kup” lub „Sprzedaj”. Wskaźnik ten jest obliczany na podstawie średniej ruchomej.

#### Strona 4
Na czwartej stronie, jako dodatkowe informacje, znajduje się tabela 25 najbardziej aktywnych obecnie akcji giełdowych. Tabela ta jest pobierana i generowana z pliku **25_most_active_stocks.csv**.

## Licencja

Ten projekt jest objęty licencją MIT. Szczegóły można znaleźć w pliku LICENSE.txt.

## Wkład

Zachęcamy do przesyłania zgłoszeń lub pull requestów, jeśli masz sugestie dotyczące projektu lub pomysł na ulepszenia.

## Autorzy

Gabriela Kiwacka - Współtwórca - https://github.com/GabrielaKiwacka

Piotr Greń - Współtwórca - https://github.com/PiotrGren
