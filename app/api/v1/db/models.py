import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base,  sessionmaker

load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=os.getenv("DB_USERNAME", ""),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", ""),
    database=os.getenv("DB_NAME", ""),
    port=os.getenv("DB_PORT", 5432),
)

engine = create_engine(url, echo=True, pool_size=80, max_overflow=15)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    student = Column(String)
    message = Column(String)
    role = Column(String)
    message_type = Column(String)
    timestamp = Column(String)


Base.metadata.create_all(bind=engine, checkfirst=True)
