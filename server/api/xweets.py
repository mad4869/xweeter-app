from flask import request, jsonify

from . import api_bp
from ..extensions import db
from ..models import Xweets, Users


@api_bp.route("/xweets", methods=["GET"], strict_slashes=False)
def get_xweets():
    xweets = db.session.execute(db.select(Xweets)).scalars()
    data = [xweet.serialize() for xweet in xweets]

    return jsonify({"success": True, "data": data}), 200


@api_bp.route("/xweets/<int:xweet_id>", methods=["GET"], strict_slashes=False)
def access_xweet(xweet_id):
    xweet = db.session.execute(
        db.select(Xweets).filter_by(xweet_id=xweet_id)
    ).scalar_one_or_none()
    data = xweet.serialize()

    return jsonify({"success": True, "data": data}), 200


@api_bp.route(
    "/users/<int:user_id>/xweets", methods=["GET", "POST"], strict_slashes=False
)
def access_xweets_by_user(user_id):
    if request.method == "POST":
        data = request.get_json()
        body = data["body"]

        xweet = Xweets(user_id=user_id, body=body)

        try:
            db.session.add(xweet)
            db.session.commit()
        except:
            db.session.rollback()

            return jsonify({"success": False, "message": "Failed to add the task"}), 500
        else:
            return jsonify({"success": True, "data": xweet.serialize()}), 201

    xweets = db.session.execute(
        db.select(Xweets)
        .join(Users, Xweets.user_id == Users.user_id)
        .filter(Users.user_id == user_id)
        .order_by(Xweets.created_at.desc())
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
