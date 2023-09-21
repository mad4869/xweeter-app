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
