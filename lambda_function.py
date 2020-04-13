import json
import base64
import os
import urllib
import datetime
import boto3
from urllib import request, parse
from datetime import date

def lambda_handler(event, context):
    today = date.today()
    today = date(2020, 4, 15)
    tomorrow = today + datetime.timedelta(days=1)

    bin_data = {
            "black" : {
                "start" : date(2020, 1, 2),
                "frequency" : 2
                },
            "brown" : {
                "start" : date(2020, 1, 23),
                "frequency" : 4
                },
            "blue" : {
                "start" : date(2020, 1, 23),
                "frequency" : 4
                }
            }

    these_bins = []
    for bin_colour, bin_info in bin_data.items():
        days_between = tomorrow - bin_info["start"]

        if (days_between.days % (bin_info["frequency"] * 7) == 0):
            these_bins.append(bin_colour)

    if (len(these_bins) > 0):
        bullet = "👉"
        message = f"Hey, this is The Bindicator\n\nThe following bins will be collected tomorrow:\n  {bullet} " + (f"\n  {bullet} ".join(these_bins))
        message = message + "\n\nTo unsubscribe, send STOP to 07775785078"
        print(message)

        numbers = os.environ.get("PHONE_NUMBERS")
        number_list = numbers.split(':')

        for to_number in number_list:
            send_sms(to_number, message)

        return "SMS sent successfully!"

    print('no bins')
    return "No bins today!"

def send_sms(number, message):
    session = boto3.Session()

    client = session.client('sns')

    client.publish(PhoneNumber=number, Message=message)

# lambda_handler('n', 'n')
