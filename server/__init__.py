from flask import Flask

from .extensions import *
from .models import *
from .routes import routes
from .config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(routes)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)
    jwt_manager.init_app(app)
    socket.init_app(app)

    return app


app = create_app()
