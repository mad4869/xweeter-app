from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from minio import Minio
from os import environ, path
from dotenv import load_dotenv

basedir = path.dirname(__file__)
load_dotenv(path.join(path.dirname(basedir), ".env"))

# Database engine
db = SQLAlchemy()

# Database migration manager
migrate = Migrate()

# Password hash generator
bcrypt = Bcrypt()

# CORS
cors = CORS()

# User auth manager
login_manager = LoginManager()
jwt_manager = JWTManager()

# Object storage
mc = Minio(
    "localhost:9000",
    access_key=environ.get("MINIO_ACCESS_KEY"),
    secret_key=environ.get("MINIO_SECRET_KEY"),
    secure=False,
)
