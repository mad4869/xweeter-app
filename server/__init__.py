from flask import Flask

from .extensions import *


def create_app():
    from .config import Config
    from .models import *

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app


app = create_app()
