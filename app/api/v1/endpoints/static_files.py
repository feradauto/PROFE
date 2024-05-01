from fastapi import APIRouter, Request, Path
from fastapi.responses import FileResponse



router = APIRouter()

SUPPORTED_IMAGE_FORMATS=['jpeg','jpg','gif','png']

SUPPORTED_AUDIO_FORMATS=['basic','mp4','mpeg','ogg','mp3','aac']

@router.get("/imagen/{file_name}")
async def get_imagen(file_name: str = Path(...) ):
    format = file_name.split('.')[1]
    if format in SUPPORTED_IMAGE_FORMATS:
        return FileResponse(f"./app/static/images/{file_name}", media_type=f"image/{format}")
    else:
        raise Exception("Invalid file format")

@router.get("/audio/{file_name}")
async def get_audio(file_name: str = Path(...)):
    format = file_name.split('.')[1]
    print(f"format {format}")
    if format in SUPPORTED_AUDIO_FORMATS:
        return FileResponse(f"./app/static/audio/{file_name}", media_type=f"audio/{format}")
    else:
        raise Exception("Invalid file format")
