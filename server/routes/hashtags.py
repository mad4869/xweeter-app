from flask import request, jsonify
from datetime import datetime, timedelta

from . import routes
from ..extensions import db
from ..models import Xweet, User, Hashtag, hashtag_xweet


@routes.route("/hashtags", methods=["GET"], strict_slashes=False)
def get_hashtags():
    hashtags = db.session.execute(
        db.select(Hashtag)
        .join(hashtag_xweet, Hashtag.hashtag_id == hashtag_xweet.c.hashtag_id)
        .join(Xweet, hashtag_xweet.c.xweet_id == Xweet.xweet_id)
    ).scalars()
    data = [hashtag.serialize() for hashtag in hashtags]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/trending", methods=["GET"], strict_slashes=False)
def get_trending():
    trending = db.session.execute(
        db.select(
            Hashtag.hashtag_id,
            Hashtag.body,
            db.func.count(Xweet.xweet_id).label("xweet_count"),
        )
        .join(hashtag_xweet, Hashtag.hashtag_id == hashtag_xweet.c.hashtag_id)
        .join(Xweet, hashtag_xweet.c.xweet_id == Xweet.xweet_id)
        .filter(hashtag_xweet.c.created_at >= datetime.now() - timedelta(days=7))
        .group_by(Hashtag.hashtag_id)
    ).fetchall()
    data = [
        {
            "hashtag_id": hashtag[0],
            "body": hashtag[1],
            "xweet_count": hashtag[2],
        }
        for hashtag in trending
    ]

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
