from flask import request, jsonify

from . import routes
from ..extensions import db
from ..models import Xweet, User, Hashtag, hashtag_xweet


@routes.route("/hashtags", methods=["GET"], strict_slashes=False)
def get_hashtags():
    hashtags = db.session.execute(
        db.select(Hashtag).join(
            hashtag_xweet, Hashtag.hashtag_id == hashtag_xweet.c.hashtag_id
        )
    ).scalars()
    data = [hashtag.serialize() for hashtag in hashtags]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/hashtags/<string:tag>", methods=["GET"], strict_slashes=False)
def get_xweets_by_tag(tag):
    xweets = db.session.execute(
        db.select(Xweet)
        .join(hashtag_xweet, Xweet.xweet_id == hashtag_xweet.c.xweet_id)
        .join(Hashtag, hashtag_xweet.c.hashtag_id == Hashtag.hashtag_id)
        .filter(Hashtag.body == tag)
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
