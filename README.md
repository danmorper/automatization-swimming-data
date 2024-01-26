# Swimming Competition Data Automation

This repository contains a set of Python scripts that automate the process of collecting, processing, and organizing swimming competition data from various websites. The scripts use web scraping, data extraction, and file management techniques to achieve this automation.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [File Structure](#file-structure)

## Features

- **Web Scraping**: Automated web scraping to extract competition data from multiple websites.
- **Data Processing**: Conversion of extracted data from PDF format to CSV, with data type conversions and cleaning.
- **Data Organization**: Merging CSV files for different cities and organizing PDFs into folders.
- **Configurable**: Easily adaptable for different competition websites and data formats.
- **Headless Browsing**: Utilizes headless browsers for web scraping, reducing visual disturbance.

## Prerequisites

Before using these scripts, make sure you have the following dependencies installed:

- Python 3.x
- Selenium
- Pandas
- Requests
- Tabula
- Firefox WebDriver (for Selenium)

You can install the required Python packages using `pip`:
`pip install selenium pandas requests tabula-py`



## Getting Started

1. Clone this repository to your local machine:

`git clone https://github.com/danmorper/swimming-competition-automation.git`

2. Navigate to the project directory:
`cd swimming-competition-automation`

3. Install the necessary Python packages as mentioned in the prerequisites.

4. In order to download the list of all swimming teams in Spain from this website, https://rfen.es/es/clubs, run: 
`python clubs.py`
The results can be seen in clubs.csv
5. In order to download all the results of the competitions in pdf from this website, https://www.fan.es/, run:
`python main_workflow.py`
the result can be seen in pdfs folder

6. In order to convert pdfs to csvs, run 
`python pdf_csv.py`
the result can be seen in cvs folder
## Structure
The repository is organized as follows:

- main_workflow.py: Main control script to execute the entire workflow.
- pdf_to_csv_converter.py: Script to process PDF files and convert them to CSV.
- merge_csv_files.py: Script to merge CSV files for different cities.
- url_scraper.py: Script for web scraping and URL extraction.
- additional_url_scraper.py: Script to scrape additional URLs based on collected data.
- functions200m.py, functions100m.py, functions50m.py: External functions for PDF data extraction.
- README.md: This documentation file.