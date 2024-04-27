from fastapi import APIRouter, Request, Form
from loguru import logger
import requests

import os
import mimetypes
import requests
import base64
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from app.api.v1.agents.orchestrator_agent import OrchestratorAgent
load_dotenv()

ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN", "")

router = APIRouter()


@router.post("/message")
async def message(request: Request):
    form_data = await request.form()
    logger.info(form_data)
    credentials = f"{ACCOUNT_SID}:{AUTH_TOKEN}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    if 'NumMedia' in form_data and form_data['NumMedia'] != '0':
        if "image" in form_data['MediaContentType0']:
            extension = "jpg"
        elif "audio" in form_data['MediaContentType0']:
            extension = "mp3"
        elif "video" in form_data['MediaContentType0']:
            extension = "mp4"
        filename = form_data['SmsMessageSid'] + '.' +extension
        
        with open( filename, 'wb') as f:
            response = requests.get(form_data['MediaUrl0'],headers=headers,stream=True)
            response.raise_for_status()
            f.write(response.content)

    whatsapp = form_data['From']
    message = form_data['Body']
    orchestrator=OrchestratorAgent(whatsapp=whatsapp)
    answer=orchestrator.run(message)


    logger.info(answer)
    return answer

