import os
from dotenv import load_dotenv
import logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS = False
TESTING = True
SECRET_KEY = os.getenv("SECRET_KEY")

# Email configuration
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = os.getenv("MAIL_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 300))


MAIL_SUPRESS_SEND = True

# Suppress sending emails and disable logging during tests
if TESTING:
    MAIL_SUPRESS_SEND = True
    logging.disable(logging.CRITICAL)

# Disable CSRF protection during tests
WTF_CSRF_ENABLED = False
