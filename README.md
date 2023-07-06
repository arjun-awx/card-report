# card-report
Generate Airwallex Card Transactions Report. This script fetches transactions data from [Airwallex Issuing Transcations API](https://www.airwallex.com/docs/api#/Issuing/Transactions/_api_v1_issuing_transactions/get).

## Setup

Install dependencies:  
`python3 -m pip install requests`  
or  
`pip install -r requirements.txt`  
  
Update report.cfg file with [Airwallex API key and Client ID](https://www.airwallex.com/docs/api#/Getting_Started).

## Usage

To see supported arguments, run:  
`python3 create-card-report.py -h`  

To create a report with yesterday's transactions, run:  
`python3 create-card-report.py`  
or  
`python3 create-card-report.py -d yesterday`  

To create a report with today's transactions, run:  
`python3 create-card-report.py -d today`  

To create a report with transcations on a specific date, run:  
`python3 create-card-report.py -d YYYY-MM-DD`  

To create a monthly report, run:  
`python3 create-card-report.py -d last_month`  
or  
`python3 create-card-report.py -d this_month`    

## Output

Output CSV file is created in the same directory.

Output file naming convention is `report-YYYY-MM.csv` for monthly report and `report-YYYY-MM-DD.csv` for report for a specific date.
