import os

from twilio.rest import Client
from dotenv import load_dotenv
from loguru import logger
load_dotenv()

ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_NUMBER=os.getenv("TWILIO_NUMBER", "")

account_sid = ACCOUNT_SID
auth_token = AUTH_TOKEN
client = Client(account_sid, auth_token)

def send_message(to_number,body_text,from_number=TWILIO_NUMBER):
  try:
    message = client.messages.create(
      from_=f"whatsapp:{from_number}",
      body=body_text,
      to=f"whatsapp:{to_number}"
      )
    logger.info(f"Message sent to {to_number}: {message.body}")
  except Exception as e:
    logger.error(f"Error sending message to {to_number}: {e}")
