import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read Twilio credentials from environment variables
user = os.getenv('POSTGRES_USER')
db = os.getenv('POSTGRES_DB')
password = os.getenv('POSTGRES_PASSWORD')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
host = os.getenv('POSTGRES_HOST')
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    user, password, host, db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
