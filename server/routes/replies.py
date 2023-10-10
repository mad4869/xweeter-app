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
from ..models import Xweet, User, Reply
from ..constants import MINIO_BUCKET


@routes.route("/xweets/<int:xweet_id>/replies", methods=["GET"], strict_slashes=False)
def get_replies_by_xweet(xweet_id):
    replies = db.session.execute(
        db.select(Reply)
        .join(Xweet, Reply.xweet_id == Xweet.xweet_id)
        .join(User, Xweet.user_id == User.user_id)
        .filter(Reply.xweet_id == xweet_id)
        .order_by(Reply.created_at)
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


@routes.route(
    "/users/<int:user_id>/replies", methods=["GET", "POST"], strict_slashes=False
)
@jwt_required()
def access_replies_by_user(user_id):
    if request.method == "POST":
        data = request.get_json()
        xweet_id = data.get("xweet_id")
        body = data.get("body")
        media_url = data.get("media")

        if not body and not media_url:
            return (
                jsonify({"success": False, "message": "Reply cannot be empty"}),
                400,
            )

        if media_url:
            media_data = base64.b64decode(media_url.split(",")[1])
            media_stream = io.BytesIO(media_data)
            media_id = uuid.uuid4()
            media_ext = imghdr.what(media_stream)
            OBJECT_NAME = f"{media_id}.{media_ext}"

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

        reply = Reply(user_id=user_id, xweet_id=xweet_id, body=body, media=media)

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


@routes.route(
    "/users/<int:user_id>/replies/<int:reply_id>",
    methods=["GET", "PUT", "DELETE"],
    strict_slashes=False,
)
@jwt_required()
def access_reply_by_user(user_id, reply_id):
    reply = db.session.execute(
        db.select(Reply).filter(Reply.reply_id == reply_id)
    ).scalar_one_or_none()

    if reply is None:
        return (
            jsonify({"success": False, "message": "Reply not found"}),
            404,
        )

    if request.method == "PUT":
        data = request.get_json()
        body = data.get("body")
        media_url = data.get("media")

        if not body and not media_url:
            return (
                jsonify({"success": False, "message": "Reply cannot be empty"}),
                400,
            )

        if media_url:
            media_data = base64.b64decode(media_url.split(",")[1])
            media_stream = io.BytesIO(media_data)
            media_id = uuid.uuid4()
            media_ext = imghdr.what(media_stream)
            OBJECT_NAME = f"{media_id}.{media_ext}"

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

        try:
            reply.body = body
            reply.media = media
            reply.updated_at = datetime.now()
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
            return jsonify({"success": True, "data": reply.serialize()}), 201

    elif request.method == "DELETE":
        try:
            db.session.delete(reply)
            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to delete the reply"}),
                500,
            )
        else:
            return (
                jsonify({"success": True, "data": reply.serialize()}),
                201,
            )

    return jsonify({"success": True, "data": reply.serialize()}), 200
