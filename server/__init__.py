from flask import Flask

from .extensions import *


def create_app():
    from .config import Config
    from .models import Users, Xweets, Followings, Rexweets, Likes, Replies
    from .api import api_bp

    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(api_bp)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)

    return app


app = create_app()
