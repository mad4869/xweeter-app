from flask import Flask
from flask_admin.contrib.sqla import ModelView

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
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Xweet, db.session))
    admin.add_view(ModelView(Rexweet, db.session))
    admin.add_view(ModelView(Like, db.session))
    admin.add_view(ModelView(Reply, db.session))
    admin.add_view(ModelView(Hashtag, db.session))

    return app


app = create_app()
