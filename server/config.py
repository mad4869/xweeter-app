from os import environ, path
from dotenv import load_dotenv
import datetime

basedir = path.dirname(__file__)
load_dotenv(path.join(path.dirname(basedir), ".env"))


class Config:
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    ENVIRONMENT = environ.get("ENVIRONMENT")
    SECRET_KEY = environ.get("SECRET_KEY")

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)
