from flask import request, jsonify

from . import api_bp
from ..extensions import db
from ..models import Xweets


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
