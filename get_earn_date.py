# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import json
import requests
import datetime
from datetime import date

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException

two_weeks_from_now = (date.today() + datetime.timedelta(days=14)).strftime("%Y%m%d")

api_url = 'https://api.earningscalendar.net/?date='+two_weeks_from_now
print(api_url)
headers = {'Content-Type': 'application/json'}

def get_account_info():

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

print(get_account_info())

up_earns = get_account_info()
stock = ''
for up_earn in up_earns:
    stock = up_earn['ticker']+','+stock

print(stock)

to_emails = [
    To('<TO_EMAIL>', '<NAME>'),
    To('<TO_EMAIL>', '<NAME>')
]

message = Mail(
    from_email='<FROM_EMAIL>',
    to_emails=to_emails,
    subject='Upcoming Earnings '+two_weeks_from_now,
    html_content='<strong>'+stock+'</strong>')
try:
    sg = SendGridAPIClient('<API_KEY_GOES_HERE')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)