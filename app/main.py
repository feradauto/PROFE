from fastapi import FastAPI
from app.api.v1.api import api_router
import uvicorn
import os
from loguru import logger
import sys
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles


load_dotenv()

DEFAULT_LOG_LEVEL = "DEBUG"
API_V1_STR = "/api/v1"

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", default=DEFAULT_LOG_LEVEL))

app = FastAPI()
app.include_router(api_router, prefix=API_V1_STR)
app.mount("/static", StaticFiles(directory="./app/static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3001,
        log_level=os.getenv("LOG_LEVEL", default=DEFAULT_LOG_LEVEL).lower(),
    )