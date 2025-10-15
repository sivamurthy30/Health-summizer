import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'symptom_checker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Rate limiting configuration
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Request timeout for API calls (seconds)
    API_TIMEOUT = 30