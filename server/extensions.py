from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Database engine
db = SQLAlchemy()

# Database migration manager
migrate = Migrate()

# Password hash generator
bcrypt = Bcrypt()
