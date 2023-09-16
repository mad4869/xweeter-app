from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import routes, logging
from ..extensions import db, jwt_manager
from ..models import User, follow


@routes.route(
    "/users/<int:user_id>/following", methods=["GET", "POST"], strict_slashes=False
)
@jwt_required()
def access_user_following(user_id):
    if request.method == "POST":
        return

    followings = db.session.execute(
        db.select(User)
        .join(follow, User.user_id == follow.c.followed_id)
        .filter(follow.c.follower_id == user_id)
        .order_by(follow.c.created_at.desc())
    ).scalars()
    data = []
    for following in followings:
        serial = following.serialize()
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route(
    "/users/<int:user_id>/followers", methods=["GET", "POST"], strict_slashes=False
)
@jwt_required()
def access_user_followers(user_id):
    if request.method == "POST":
        return

    followers = db.session.execute(
        db.select(User)
        .join(follow, User.user_id == follow.c.follower_id)
        .filter(follow.c.followed_id == user_id)
        .order_by(follow.c.created_at.desc())
    ).scalars()
    data = []
    for follower in followers:
        serial = follower.serialize()
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200
