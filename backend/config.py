import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    POSTGRES_URI = os.getenv('POSTGRES_URI', 'postgresql://localhost/criminalcode')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't') 