import json
import base64
import os
import urllib
import datetime
from urllib import request, parse
from datetime import date

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

def lambda_handler(event, context):
    today = date.today()
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
        body = "The following bins will be collected tomorrow: " + (", ".join(these_bins))
        print(body)

        from_number = '+19045670539'
        to_number = '+447775785078'

        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        post_params = {"To": to_number, "From": from_number, "Body": body}

        data = parse.urlencode(post_params).encode()
        req = request.Request(populated_url)

        authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))

        try:
            # perform HTTP POST request
            with request.urlopen(req, data) as f:
                print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
        except Exception as e:
            # something went wrong!
            return e

        return "SMS sent successfully!"

    return "No bins today!"
