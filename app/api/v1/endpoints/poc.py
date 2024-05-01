from fastapi import APIRouter, Request, Path
from fastapi.responses import FileResponse
from app.api.v1.twilio.whats import send_message
import os
from dotenv import load_dotenv

load_dotenv()

TO_NUMBER = os.getenv("TO_NUMBER","")

router = APIRouter()

@router.post("/media")
async def send_media(request: Request):
    data = await request.json()
    send_message(TO_NUMBER,data['url'],False)