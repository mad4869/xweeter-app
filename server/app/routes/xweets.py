from flask import request, jsonify
from flask_jwt_extended import jwt_required
from minio.error import S3Error
from datetime import datetime

from . import routes
from ..extensions import db, mc
from ..models import Xweet, User, Hashtag, hashtag_xweet
from ..constants import MINIO_BUCKET
from ..utils.manage_file import manage_file


@routes.route("/xweets/<int:xweet_id>", methods=["GET"], strict_slashes=False)
def access_xweet(xweet_id):
    xweet = db.session.execute(
        db.select(Xweet).filter(Xweet.xweet_id == xweet_id)
    ).scalar_one_or_none()

    if xweet is None:
        return jsonify({"success": False, "message": "Xweet is not found"}), 404

    data = xweet.serialize()
    data.update(
        {
            "username": xweet.users.username,
            "full_name": xweet.users.full_name,
            "profile_pic": xweet.users.profile_pic,
        }
    )

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>/xweets", methods=["GET"], strict_slashes=False)
def get_xweets_by_user(user_id):
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


@routes.route("/users/<int:user_id>/xweets", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_xweet(user_id):
    data = request.get_json()
    body = data.get("body")
    media_url = data.get("media")
    hashtags = data.get("hashtags")

    if not body and not media_url:
        return (
            jsonify({"success": False, "message": "Xweet cannot be empty"}),
            400,
        )

    if media_url:
        media_data, media_stream, OBJECT_NAME = manage_file(media_url)

        try:
            mc.put_object(MINIO_BUCKET, OBJECT_NAME, media_stream, len(media_data))
            media = mc.presigned_get_object(MINIO_BUCKET, OBJECT_NAME)
        except S3Error as err:
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
        media = None

    xweet = Xweet(user_id=user_id, body=body, media=media)

    try:
        db.session.add(xweet)
        db.session.commit()

        if len(hashtags) != 0:
            for tag in hashtags:
                existing_tag = db.session.execute(
                    db.select(Hashtag).filter(Hashtag.body == tag)
                ).scalar_one_or_none()

                if existing_tag:
                    db.session.execute(
                        hashtag_xweet.insert().values(
                            xweet_id=xweet.xweet_id,
                            hashtag_id=existing_tag.hashtag_id,
                        )
                    )
                    db.session.commit()
                else:
                    hashtag = Hashtag(body=tag)

                    db.session.add(hashtag)
                    db.session.commit()

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
    else:
        return jsonify({"success": True, "data": xweet.serialize()}), 201


@routes.route(
    "/users/<int:user_id>/xweets/<int:xweet_id>",
    methods=["PUT", "DELETE"],
    strict_slashes=False,
)
@jwt_required()
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
        media_url = data.get("media")
        hashtags = data.get("hashtags")

        if not body and not media_url:
            return (
                jsonify({"success": False, "message": "Xweet cannot be empty"}),
                400,
            )

        if media_url and media_url != xweet.media:
            media_data, media_stream, OBJECT_NAME = manage_file(media_url)

            try:
                mc.put_object(MINIO_BUCKET, OBJECT_NAME, media_stream, len(media_data))
                media = mc.presigned_get_object(MINIO_BUCKET, OBJECT_NAME)
            except S3Error as err:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": f"Error occured during the process: {str(err)}",
                        }
                    ),
                    500,
                )
        elif media_url and media_url == xweet.media:
            media = xweet.media
        else:
            media = None

        try:
            xweet.body = body
            xweet.media = media
            xweet.updated_at = datetime.now()
            db.session.commit()

            if len(hashtags) != 0:
                for tag in hashtags:
                    existing_tag = db.session.execute(
                        db.select(Hashtag).filter(Hashtag.body == tag)
                    ).scalar_one_or_none()

                    if existing_tag:
                        tag_already_in_xweet = db.session.execute(
                            db.select(hashtag_xweet)
                            .filter(
                                hashtag_xweet.c.hashtag_id == existing_tag.hashtag_id
                            )
                            .filter(hashtag_xweet.c.xweet_id == xweet_id)
                        ).scalar_one_or_none()

                        if tag_already_in_xweet:
                            pass
                        else:
                            db.session.execute(
                                hashtag_xweet.insert().values(
                                    xweet_id=xweet.xweet_id,
                                    hashtag_id=existing_tag.hashtag_id,
                                )
                            )
                            db.session.commit()
                    else:
                        hashtag = Hashtag(body=tag)

                        db.session.add(hashtag)
                        db.session.commit()

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
