# card-report
Generate Card Transaction Report

To get started, install dependencies:
python3 -m pip install requests

Update report.cfg file with Airwallex API key and Client ID.

To create a report with yesterday's transactions, run:
python3 create-card-report.py
or
python3 create-card-report.py -d yesterday

To create a report with today's transactions, run:
python3 create-card-report.py -d today

Output CSV file is created in the same directory.
Output file naming convention is report-YYYY-MM-DD.csv
