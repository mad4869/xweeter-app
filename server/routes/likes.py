from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import routes
from ..extensions import db
from ..models import Xweet, User, Like


@routes.route(
    "/xweets/<int:xweet_id>/likes", methods=["GET", "POST"], strict_slashes=False
)
# @jwt_required()
def access_likes_by_xweet(xweet_id):
    if request.method == "POST":
        data = request.get_json()
        user_id = data.get("userId")

        like = Like(user_id=user_id, xweet_id=xweet_id)

        try:
            db.session.add(like)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to like xweet"}),
                500,
            )
        else:
            return jsonify({"success": True, "data": like.serialize()}), 201

    likes = db.session.execute(
        db.select(Like)
        .join(Xweet, Like.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Like.xweet_id == xweet_id)
        .order_by(Like.created_at.desc())
    ).scalars()
    data = []
    for like in likes:
        serial = like.serialize()
        serial.update(
            {
                "body": like.xweets.body,
                "media": like.xweets.media,
                "username": like.users.username,
                "full_name": like.users.full_name,
                "profile_pic": like.users.profile_pic,
                "og_user_id": like.xweets.users.user_id,
                "og_username": like.xweets.users.username,
                "og_full_name": like.xweets.users.full_name,
                "og_profile_pic": like.xweets.users.profile_pic,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/likes", methods=["GET"], strict_slashes=False)
# @jwt_required()
def get_likes_by_user(user_id):
    start = int(request.args.get("start", 0))
    size = int(request.args.get("size", 10))

    likes = db.session.execute(
        db.select(Like)
        .join(Xweet, Like.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Like.user_id == user_id)
        .order_by(Like.created_at.desc())
    ).scalars()
    data = []
    for like in likes:
        serial = like.serialize()
        serial.update(
            {
                "body": like.xweets.body,
                "media": like.xweets.media,
                "username": like.users.username,
                "full_name": like.users.full_name,
                "profile_pic": like.users.profile_pic,
                "og_user_id": like.xweets.users.user_id,
                "og_username": like.xweets.users.username,
                "og_full_name": like.xweets.users.full_name,
                "og_profile_pic": like.xweets.users.profile_pic,
            }
        )
        data.append(serial)

    sorted_data = sorted(data, key=lambda xweet: xweet["created_at"], reverse=True)

    end = min(start + size, len(sorted_data))

    sliced_data = sorted_data[start:end]

    return jsonify({"success": True, "data": sliced_data}), 200
