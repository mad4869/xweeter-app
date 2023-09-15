from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import routes
from ..extensions import db
from ..models import Xweet, User, Hashtag


@routes.route("/xweets", methods=["GET"], strict_slashes=False)
def get_xweets():
    xweets = db.session.execute(db.select(Xweet)).scalars()
    data = [xweet.serialize() for xweet in xweets]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/xweets/<int:xweet_id>", methods=["GET"], strict_slashes=False)
def access_xweet(xweet_id):
    xweet = db.session.execute(
        db.select(Xweet).filter(Xweet.xweet_id == xweet_id)
    ).scalar_one_or_none()
    data = xweet.serialize()

    return jsonify({"success": True, "data": data}), 200


@routes.route(
    "/users/<int:user_id>/xweets", methods=["GET", "POST"], strict_slashes=False
)
@jwt_required()
def access_xweets_by_user(user_id):
    if request.method == "POST":
        data = request.get_json()
        body = data["body"]
        media = data["media"]
        hashtag_body = data["hashtag"]

        xweet = Xweet(user_id=user_id, body=body, media=media)
        hashtag = Hashtag(body=hashtag_body)

        try:
            db.session.add(xweet)
            db.session.add(hashtag)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to post the xweet"}),
                500,
            )
        else:
            return jsonify({"success": True, "data": xweet.serialize()}), 201

    xweets = db.session.execute(
        db.select(Xweet)
        .join(User, Xweet.user_id == User.user_id)
        .filter(User.user_id == user_id)
        .order_by(Xweet.created_at.desc())
    ).scalars()
    data = []
    for xweet in xweets:
        serial = xweet.serialize()
        serial.update(
            {
                "username": xweet.users.username,
                "full_name": xweet.users.full_name,
                "profile_pic": xweet.users.profile_pic,
            }
        )
        data.append(serial)

    return jsonify({"success": True, "data": data}), 200
