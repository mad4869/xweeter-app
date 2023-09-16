from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import routes
from ..extensions import db
from ..models import User


@routes.route("/users", methods=["GET"], strict_slashes=False)
# @jwt_required()
def get_users():
    users = db.session.execute(db.select(User)).scalars()
    data = [user.serialize() for user in users]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
# @jwt_required()
def access_user(user_id):
    user = db.session.execute(
        db.select(User).filter(User.user_id == user_id)
    ).scalar_one_or_none()
    data = user.serialize()

    return jsonify({"success": True, "data": data}), 200
