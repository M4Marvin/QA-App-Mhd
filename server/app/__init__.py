from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import logging
import os

# Create the Flask app object
app = Flask(__name__)

# Set configuration variables
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)

# Initialize the database connection
db = SQLAlchemy(app)

# Initialize the database migration management
migrate = Migrate(app, db)

# Initialize the mailer
mail = Mail(app)

CORS(app)

# Add logging configuration using the variables from config.py
logging.basicConfig(
    level=app.config["LOGGING_LEVEL"],
    format=app.config["LOGGING_FORMAT"],
    datefmt=app.config["LOGGING_DATEFMT"],
    handlers=[
        logging.FileHandler(
            os.path.join(app.config["LOGGING_LOCATION"], app.config["LOGGING_FILENAME"])
        ),
        logging.StreamHandler(),
    ],
)


from app import routes, models, errors
