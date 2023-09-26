from flask import request, jsonify
from flask_jwt_extended import jwt_required
from minio.error import S3Error
from datetime import datetime
import base64
import io
import uuid
import imghdr

from . import routes
from ..extensions import db, mc
from ..models import Xweet, User, Hashtag, hashtag_xweet

BUCKET = "xweeter"


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
# @jwt_required()
def access_xweets_by_user(user_id):
    if request.method == "POST":
        data = request.get_json()
        body = data.get("body")
        media = data.get("media")
        hashtags = data.get("hashtags")

        if not media and len(hashtags) == 0:
            xweet = Xweet(user_id=user_id, body=body)

            try:
                db.session.add(xweet)
                db.session.commit()
            except:
                db.session.rollback()

                return (
                    jsonify({"success": False, "message": "Failed to post the xweet"}),
                    500,
                )
            else:
                return jsonify({"success": True, "data": xweet.serialize()}), 201
        elif len(hashtags) == 0:
            media_url = data.get("media")
            media_data = base64.b64decode(media_url.split(",")[1])
            media_stream = io.BytesIO(media_data)
            media_id = uuid.uuid4()
            media_ext = imghdr.what(media_stream)
            OBJECT_NAME = f"{media_id}.{media_ext}"

            try:
                mc.put_object(BUCKET, OBJECT_NAME, media_stream, len(media_data))
                media = mc.presigned_get_object(BUCKET, OBJECT_NAME)

                xweet = Xweet(user_id=user_id, body=body, media=media)

                db.session.add(xweet)
                db.session.commit()
            except S3Error as err:
                db.session.rollback()

                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f"Error occured during the process: {str(err)}",
                        }
                    ),
                    500,
                )
            else:
                return jsonify({"success": True, "data": xweet.serialize()}), 201
        else:
            try:
                db.session.add(xweet)
                db.session.commit()
            except Exception as err:
                db.session.rollback()

                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f"Error occured during the process: {str(err)}",
                        }
                    ),
                    500,
                )

            tags = data.get("hashtags")

            for tag in tags:
                hashtag = Hashtag(body=tag)

                try:
                    db.session.add(hashtag)
                    db.session.execute(
                        hashtag_xweet.insert().values(
                            xweet_id=xweet.xweet_id, hashtag_id=hashtag.hashtag_id
                        )
                    )
                    db.session.commit()
                except Exception as err:
                    db.session.rollback()

                    return (
                        jsonify(
                            {
                                "success": False,
                                "message": f"Error occured during the process: {str(err)}",
                            }
                        ),
                        500,
                    )

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


@routes.route(
    "/users/<int:user_id>/xweets/<int:xweet_id>",
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False,
)
def access_xweet_by_user(user_id, xweet_id):
    xweet = db.session.execute(
        db.select(Xweet).filter(Xweet.xweet_id == xweet_id)
    ).scalar_one_or_none()

    if xweet is None:
        return (
            jsonify({"success": False, "message": "Xweet not found"}),
            404,
        )

    if request.method == "PUT":
        data = request.get_json()
        body = data.get("body")
        media = data.get("media")
        hashtags = data.get("hashtags")

        if not media and len(hashtags) == 0:
            try:
                xweet.body = body
                xweet.updated_at = datetime.now()

                db.session.commit()
            except:
                db.session.rollback()

                return (
                    jsonify({"success": False, "message": "Failed to edit the xweet"}),
                    500,
                )
            else:
                return jsonify({"success": True, "data": xweet.serialize()}), 201

    elif request.method == "DELETE":
        try:
            db.session.delete(xweet)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to delete the xweet"}),
                500,
            )
        else:
            return (
                jsonify({"success": True, "data": xweet.serialize()}),
                201,
            )

    return jsonify({"success": True, "data": xweet.serialize()}), 200
