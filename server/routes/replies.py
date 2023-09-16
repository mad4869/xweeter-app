from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import routes
from ..extensions import db
from ..models import Xweet, User, Reply


@routes.route(
    "/xweets/<int:xweet_id>/replies", methods=["GET", "POST"], strict_slashes=False
)
# @jwt_required()
def access_replies_by_xweet(xweet_id):
    if request.method == "POST":
        data = request.get_json()
        user_id = data.get("user_id")
        body = data.get("body")

        reply = Reply(user_id=user_id, xweet_id=xweet_id, body=body)

        try:
            db.session.add(reply)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to reply xweet"}),
                500,
            )
        else:
            return jsonify({"success": True, "data": reply.serialize()}), 201

    replies = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Reply.xweet_id == xweet_id)
        .order_by(Reply.created_at.desc())
    ).scalars()

    data = []

    for reply in replies:
        serial = reply.serialize()
        serial.update(
            {
                "username": reply.users.username,
                "full_name": reply.users.full_name,
                "profile_pic": reply.users.profile_pic,
                "og_user_id": reply.xweets.users.user_id,
                "og_username": reply.xweets.users.username,
                "og_full_name": reply.xweets.users.full_name,
                "og_profile_pic": reply.xweets.users.profile_pic,
                "og_body": reply.xweets.body,
                "og_media": reply.xweets.media,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/replies", methods=["GET"], strict_slashes=False)
def get_replies_by_user(user_id):
    replies = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Reply.user_id == User.user_id)
        .filter(Reply.user_id == user_id)
        .order_by(Reply.created_at.desc())
    ).scalars()

    data = []

    for reply in replies:
        serial = reply.serialize()
        serial.update(
            {
                "username": reply.users.username,
                "full_name": reply.users.full_name,
                "profile_pic": reply.users.profile_pic,
                "og_user_id": reply.xweets.users.user_id,
                "og_username": reply.xweets.users.username,
                "og_full_name": reply.xweets.users.full_name,
                "og_profile_pic": reply.xweets.users.profile_pic,
                "og_body": reply.xweets.body,
                "og_media": reply.xweets.media,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200
