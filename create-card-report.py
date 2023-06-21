import requests
import csv
import re
import argparse
import configparser

from datetime import datetime, timedelta

URI = 'https://api-demo.airwallex.com/api/v1'

config = configparser.ConfigParser()
config.read('report.cfg')


def formatted_daterange(type='yesterday', format='%Y-%m-%d'):
    start_time = 'T00:00:00.000+0000'
    end_time = 'T23:59:59.999+0000'
    
    if type == 'yesterday':
      date = datetime.now() - timedelta(1)
    elif type == 'today':
       date = datetime.now()
    
    date = date.strftime(format)
    return [date + start_time, date + end_time, date]


def get_transactions(daterange):
  print("Generating Card Transaction Report")
  
  start_date, end_date, date = formatted_daterange(daterange)

  report_filename = 'report-{}.csv'.format(date)
  with open(report_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    report_fields = [
        "Transaction Date", 
        "Transaction Time", 
        "Transaction Type", 
        "Transaction ID", 
        "Card ID", 
        "Card Nickname", 
        "Client Data", 
        "Status", 
        "Billing Amount", 
        "Billing Currency",	
        "Transaction Amount",	
        "Transaction Currency", 
        "Masked Card Number", 
        "Merchant Name", 
        "Merchant City",	
        "Merchant Country", 
        "Merchant Category Code", 
        "Posted Date", 
        "Posted Time", 
        "Failure Reason", 
        "Auth Code", 
        "Matched Authorizations", 
        "Network Transcation ID"
      ]
    
    writer.writerow(report_fields)

    token_headers = {
      'Content-Type': 'application/json',
      'x-api-key': config['airwallex']['api_key'],
      'x-client-id': config['airwallex']['client_id']
    }

    r = requests.post(URI + '/authentication/login', headers=token_headers)
    token = r.json()['token']

    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }

    page_num = 0

    while True:
      payload = {
                  'page_num': page_num, 
                  'from_created_at': start_date, 
                  'to_created_at': end_date
                }
      
      txn_request = requests.get(URI + '/issuing/transactions', params=payload, headers=headers)
      txn_response = txn_request.json()
      transactions = txn_response["items"]
      print("Processed page {}".format(page_num))

      for transaction in transactions:
        transaction_date, transaction_time, *_ = re.split('T|,|\.', transaction['transaction_date'])
        posted_date, posted_time, *_ = re.split('T|,|\.', transaction['posted_date'])       
        failure_reason = transaction.get('failure_reason', '')
        matched_authorizations = ''

        if 'matched_authorizations' in transaction:
          matched_authorizations =  ', '.join(transaction['matched_authorizations'])

        transaction_reformatted = [
            transaction_date,
            transaction_time,
            transaction['transaction_type'],
            transaction['transaction_id'],
            transaction['card_id'],
            transaction['card_nickname'],
            transaction['client_data'],
            transaction['status'],
            transaction['billing_amount'],
            transaction['billing_currency'],
            transaction['transaction_amount'],
            transaction['transaction_currency'],
            transaction['masked_card_number'],
            transaction['merchant']['name'],
            transaction['merchant']['city'],
            transaction['merchant']['country'],
            transaction['merchant']['category_code'],
            posted_date,
            posted_time,
            failure_reason,
            transaction['auth_code'],
            matched_authorizations,
            transaction['network_transaction_id']
        ]
        
        writer.writerow(transaction_reformatted)

      if txn_response['has_more']:
        page_num = page_num + 1
      else:
        print("Processing complete")
        break


if __name__ == '__main__':
  arg_desc = 'Generate Card Transaction Report'
  parser = argparse.ArgumentParser(description=arg_desc)
  parser.add_argument("-d", "--daterange", help = "specify one of \"yesterday\" or \"today\"")
  args = vars(parser.parse_args())

  if args["daterange"] == "today":
    daterange = "today"
  else:
    daterange = "yesterday"

  get_transactions(daterange)