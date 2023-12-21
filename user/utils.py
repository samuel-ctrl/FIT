import random
import logging

from django.core.mail import send_mail
from django.conf import settings

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

import smtplib
from unittest import mock

LOGGER = logging.getLogger(__name__)

def twilio_client():
    return Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(phone, otp):
    try:
        my_otp = f"Your OTP is {otp}."
        client = twilio_client()
        message = client.messages.create(
            body=my_otp,
            to=phone,
            from_=settings.TWILIO_PHONE_NUMBER,
        )
    except TwilioRestException as e:
        error_dict = {"send": False, "message": str(e)}
        error_message = ""
        if e.code == 21211:
            error_message = "Invalid phone number"
        elif e.code == 21608:
            error_message = "The number is unverified."

        if error_message:
            error_dict["message"] = error_message
        return error_dict
    return {"send": True, "message": message}

def custom_send_mail(subject: str, body: str, receiver: list):
    LOGGER.info("======  issue not solved  ===============")
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,             
            receiver,
            fail_silently=False)

    except (
            smtplib.SMTPException,
            smtplib.SMTPServerDisconnected,
            smtplib.SMTPResponseException,
            smtplib.SMTPSenderRefused,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPDataError,
        ) as e:
        return {"send": False, "message": str(e)}
    return {"send": True, "message": "Mail send Successfully."}