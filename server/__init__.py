from flask import Flask


def create_app():
    from .config import Config

    app = Flask(__name__)

    app.config.from_object(Config)

    return app


app = create_app()
