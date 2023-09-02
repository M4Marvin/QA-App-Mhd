# Load environment variables for sensitive configuration settings
# such as database URI, secret key, etc.
import os
import logging
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Define base directory path and data directory path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Database Configuration
    # Load from environment variable or use SQLite as default
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///" + os.path.join(DATA_DIR, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Turn off modification tracking

    # Application Secret Key
    # Crucial for JWT creation and session management
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Debug Configuration
    # Load from environment variable or set to False by default
    DEBUG = bool(os.getenv("DEBUG", False))

    # Mail Server Configuration
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 300))

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(DATA_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"csv", "xlsx"}

    # Logging Configuration
    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
    LOGGING_DATEFMT = "%Y-%m-%d %H:%M:%S"
    LOGGING_LOCATION = os.path.join(DATA_DIR, "logs")
    LOGGING_FILENAME = "app.log"
    LOGGING_MAX_BYTES = 1024 * 1024 * 10  # 10 MB
    LOGGING_BACKUP_COUNT = 5
    LOGGING_FORMATTER = logging.Formatter(
        fmt=LOGGING_FORMAT, datefmt=LOGGING_DATEFMT, style="%"
    )
