
import os
from django.conf import settings
from twilio.rest import Client

def send_sms(message, to_):
    

    client = Client(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN)
    message = client.messages.create(
            body = message,
            from_ = '+18303762045',
            to = '+91'+to_,
        )
    

