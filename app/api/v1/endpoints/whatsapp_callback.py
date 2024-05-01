from fastapi import APIRouter, Request
from loguru import logger
import requests

import requests
from dotenv import load_dotenv
from app.api.v1.agents.orchestrator_agent import OrchestratorAgent
from app.api.v1.helpers.db_manipulation import write_message_to_db
from app.api.v1.twilio.whats import send_message
from app.api.v1.helpers.audio import audio_response

load_dotenv()

router = APIRouter()


@router.post("/message")
async def message(request: Request):
    form_data = await request.form()
    form_data = dict(form_data)
    logger.info(form_data)

    if 'NumMedia' in form_data and form_data['NumMedia'] != '0':
        url = form_data["MediaUrl0"]
        if "image" in form_data['MediaContentType0']:
            extension = "jpg"
        elif "audio" in form_data['MediaContentType0']:
            extension = "mp3"
        elif "video" in form_data['MediaContentType0']:
            extension = "mp4"
        filename = form_data['SmsMessageSid'] + '.' +extension

        form_data["Body"] += f" {filename}: {url}"

    write_message_to_db(form_data, "student")

    whatsapp = form_data['From']
    message = form_data['Body']
    orchestrator=OrchestratorAgent(whatsapp=whatsapp)
    answer=orchestrator.run(message)

    write_message_to_db({'From':whatsapp, 'Body':answer}, "teacher")

    # get the student number
    to_number = whatsapp.replace("+", "").replace("whatsapp:", "")
    send_message(to_number=to_number, body_text=answer)

    logger.info(answer)

    audio = audio_response(whatsapp, answer)
    
    return answer
