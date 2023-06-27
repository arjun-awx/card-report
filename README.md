# card-report
Generate Airwallex Card Transactions Report

## Setup

Install dependencies:  
`python3 -m pip install requests`

Update report.cfg file with [Airwallex API key and Client ID](https://www.airwallex.com/docs/api#/Getting_Started).

## Usage

To create a report with yesterday's transactions, run:  
`python3 create-card-report.py`  
or  
`python3 create-card-report.py -d yesterday`  

To create a report with today's transactions, run:  
`python3 create-card-report.py -d today`  

To create a report with transcations from a custom date, run:  
`python3 create-card-report.py -d YYYY-MM-DD`  

## Output

Output CSV file is created in the same directory.

Output file naming convention is `report-YYYY-MM-DD.csv`
