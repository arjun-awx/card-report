import requests
import csv
import re
import argparse
import configparser
from time import sleep
from datetime import datetime, timedelta, date

URI = 'https://api.airwallex.com/api/v1'

config = configparser.ConfigParser()
config.read('report.cfg')

valid_daterange_values = ['yesterday', 'today', 'last_month', 'this_month']


def formatted_daterange(daterange='yesterday', format='%Y-%m-%d'):
    start_time = 'T00:00:00.000+0000'
    end_time = 'T23:59:59.999+0000'

    if daterange == 'yesterday':
      start_date = end_date = datetime.now() - timedelta(1)
    elif daterange == 'today':
      start_date = end_date = datetime.now()
    elif daterange == 'last_month':
      first_day_of_this_month = date.today().replace(day=1)
      end_date = first_day_of_this_month - timedelta(days=1)  # last day of last month
      start_date = end_date.replace(day=1)  # first day of last month
    elif daterange == 'this_month':
      end_date = date.today()
      start_date = end_date.replace(day=1)
    else:
        start_date = end_date = daterange

    start_date = start_date.strftime(format) + start_time
    end_date = end_date.strftime(format) + end_time

    return [start_date, end_date]


def get_transactions(daterange='yesterday'):
  transcation_count = 0
  start_date, end_date = formatted_daterange(daterange)
  print('Fetching transcations from {} to {}'.format(start_date, end_date))

  if daterange == 'this_month' or daterange == 'last_month':
    report_filename = 'report-{}.csv'.format(start_date.rsplit('-', 1)[0])
  else:
    report_filename = 'report-{}.csv'.format(start_date.split('T')[0])

  with open(report_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    report_fields = [
        'Transaction Date',
        'Transaction Time',
        'Transaction Type',
        'Transaction ID',
        'Card ID',
        'Card Nickname',
        'Client Data',
        'Status',
        'Billing Amount',
        'Billing Currency',
        'Transaction Amount',
        'Transaction Currency',
        'Masked Card Number',
        'Merchant Name',
        'Merchant City',
        'Merchant Country',
        'Merchant Category Code',
        'Posted Date',
        'Posted Time',
        'Failure Reason',
        'Auth Code',
        'Matched Authorizations',
        'Network Transcation ID'
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
      sleep(0.05)
      txn_response = txn_request.json()
      transactions = txn_response['items']
      transcation_count = transcation_count + len(transactions)

      print('Processed page {}'.format(page_num))

      for transaction in transactions:
        transaction_date, transaction_time, *_ = re.split(r'T|,|\.', transaction['transaction_date'])
        posted_date, posted_time, *_ = re.split(r'T|,|\.', transaction['posted_date'])
        failure_reason = transaction.get('failure_reason', '')
        matched_authorizations = ''

        if 'matched_authorizations' in transaction:
          matched_authorizations = ', '.join(transaction['matched_authorizations'])
        
        if 'client_data' not in transaction:
          transaction['client_data'] = ''

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
        print('Processing complete. Transcation count: {}'.format(transcation_count))
        break


if __name__ == '__main__':
  arg_desc = 'Generate Card Transaction Report'
  parser = argparse.ArgumentParser(description=arg_desc)
  parser.add_argument('-d', '--daterange', nargs='?', help='specify one of {} \
                      or custom date in YYYY-MM-DD format'.format(str(valid_daterange_values)[1:-1]))
  args = vars(parser.parse_args())

  if args['daterange']:
    if args['daterange'] in valid_daterange_values:
      daterange = args['daterange']
    else:
      try:
          daterange = date.fromisoformat(args['daterange'])
      except ValueError:
          raise ValueError('Invalid daterange value')
  else:
    daterange = 'yesterday'

  print('Generating Card Transaction Report')
  get_transactions(daterange)
