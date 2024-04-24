from fastapi import FastAPI
from app.api.v1.api import api_router
import uvicorn
import os
from loguru import logger
import sys
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LOG_LEVEL = "DEBUG"
API_V1_STR = "/api/v1"

logger.remove()
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", default=DEFAULT_LOG_LEVEL))

app = FastAPI()
app.include_router(api_router, prefix=API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level=os.getenv("LOG_LEVEL", default=DEFAULT_LOG_LEVEL).lower(),
    )