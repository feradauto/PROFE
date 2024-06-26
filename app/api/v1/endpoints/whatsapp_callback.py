from fastapi import APIRouter, Request
from loguru import logger
import requests
import os
import requests
from dotenv import load_dotenv
from app.api.v1.agents.orchestrator_agent import OrchestratorAgent
from app.api.v1.helpers.db_manipulation import write_message_to_db
from app.api.v1.twilio.whats import send_message
from app.api.v1.helpers.audio import audio_response, get_and_transcribe, set_response_format

load_dotenv()

NGROK = os.getenv("NGROK_DOMIAN",None)

router = APIRouter()


@router.post("/message")
async def message(request: Request):
    form_data = await request.form()
    form_data = dict(form_data)
    logger.info(form_data)

    whatsapp = form_data['From']
    
    set_response_format(audio=False, whatsapp=whatsapp)

    if form_data['MessageType'] == 'audio':
        form_data["Body"] = get_and_transcribe(form_data['MediaUrl0'], whatsapp)
        
    elif  'NumMedia' in form_data and form_data['NumMedia'] != '0':
        url = form_data["MediaUrl0"]
        if "image" in form_data['MediaContentType0']:
            extension = "jpg"
        elif "audio" in form_data['MediaContentType0']:
            extension = "mp3"
        elif "video" in form_data['MediaContentType0']:
            extension = "mp4"
        elif "pdf" in form_data["MediaContentType0"]:
            extension = "pdf"
        filename = form_data['SmsMessageSid'] + '.' +extension

        form_data["Body"] += f" {filename}: {url}"

    write_message_to_db(form_data, "student")

    
    message = form_data['Body']
    orchestrator=OrchestratorAgent(whatsapp=whatsapp)
    answer=orchestrator.run(message)

    write_message_to_db({'From':whatsapp, 'Body':answer}, "teacher")

    # get the student number
    to_number = whatsapp.replace("+", "").replace("whatsapp:", "")
    send_message(to_number,answer)

    logger.info(answer)

    file_name = audio_response(whatsapp, answer)
    if file_name:
        file_url = "https://"+NGROK+"/api/v1/files/audio/"+file_name.split("/")[-1]
        send_message(to_number,file_url,False)

    return answer
