from flask import request, jsonify
from flask_jwt_extended import jwt_required
from minio.error import S3Error
from datetime import datetime
import base64
import io
import imghdr
import json

from . import routes
from ..extensions import db, mc
from ..models import User, Xweet

BUCKET = "xweeter"


@routes.route("/users", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_users():
    users = db.session.execute(db.select(User)).scalars()
    data = [user.serialize() for user in users]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/most-active", methods=["GET"], strict_slashes=False)
# @jwt_required()
def get_most_active_users():
    most_active_users = (
        db.session.query(
            User.user_id,
            User.username,
            User.full_name,
            User.profile_pic,
            db.func.count(Xweet.xweet_id).label("xweet_count"),
        )
        .join(Xweet, User.user_id == Xweet.user_id)
        .group_by(User.user_id, User.username, User.full_name)
        .order_by(db.func.count(Xweet.xweet_id).desc())
        .limit(2)
        .subquery()
    )
    most_active_users_xweets = (
        db.session.query(
            Xweet.body,
            most_active_users.c.user_id,
            most_active_users.c.username,
            most_active_users.c.full_name,
            most_active_users.c.profile_pic,
            db.func.row_number()
            .over(partition_by=Xweet.user_id, order_by=Xweet.created_at.desc())
            .label("row_num"),
        )
        .join(most_active_users, Xweet.user_id == most_active_users.c.user_id)
        .order_by(most_active_users.c.xweet_count)
        .subquery()
    )
    most_active_users_last_xweets = db.session.execute(
        db.select(
            most_active_users_xweets.c.body,
            most_active_users_xweets.c.user_id,
            most_active_users_xweets.c.username,
            most_active_users_xweets.c.full_name,
            most_active_users_xweets.c.profile_pic,
        ).filter(most_active_users_xweets.c.row_num == 1)
    ).fetchall()
    data = [
        {
            "body": user[0],
            "user_id": user[1],
            "username": user[2],
            "full_name": user[3],
            "profile_pic": user[4],
        }
        for user in most_active_users_last_xweets
    ]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/most-active-daily", methods=["GET"], strict_slashes=False)
def get_daily_top_users():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 0))
    offset = (page - 1) * size if size > 0 else 0

    query = (
        db.select(
            User.user_id,
            User.username,
            User.full_name,
            db.func.count(Xweet.xweet_id).label("xweet_count"),
        )
        .join(Xweet, User.user_id == Xweet.user_id)
        .filter(db.func.date(Xweet.created_at) == db.func.date(db.func.now()))
        .group_by(User.user_id, User.username, User.full_name)
        .offset(offset)
    )

    if size > 0:
        query = query.limit(size)

    users = db.session.execute(query).fetchall()
    data = [
        {
            "user_id": user[0],
            "username": user[1],
            "full_name": user[2],
            "xweet_count": user[3],
        }
        for user in users
    ]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>", methods=["GET", "PUT"], strict_slashes=False)
def access_user(user_id):
    user = db.session.execute(
        db.select(User).filter(User.user_id == user_id)
    ).scalar_one_or_none()
    data = user.serialize()

    if request.method == "PUT":
        updated_data = request.get_json()
        updated_username = updated_data.get("username")
        updated_full_name = updated_data.get("fullname")
        updated_email = updated_data.get("email")
        updated_bio = updated_data.get("bio")
        updated_profile_pic = updated_data.get("profilePic")
        updated_header_pic = updated_data.get("headerPic")

        # if updated_profile_pic:
        new_profile_pic_data = base64.b64decode(updated_profile_pic.split(",")[1])
        new_profile_pic_stream = io.BytesIO(new_profile_pic_data)
        new_profile_pic_ext = imghdr.what(new_profile_pic_stream)
        PROFILE_PIC_NAME = f"{user_id}_profile_pic.{new_profile_pic_ext}"

        try:
            mc.put_object(
                BUCKET,
                PROFILE_PIC_NAME,
                new_profile_pic_stream,
                len(new_profile_pic_data),
            )
            updated_profile_pic = mc.presigned_get_object(BUCKET, PROFILE_PIC_NAME)
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

        # if updated_header_pic:
        new_header_pic_data = base64.b64decode(updated_header_pic.split(",")[1])
        new_header_pic_stream = io.BytesIO(new_header_pic_data)
        new_header_pic_ext = imghdr.what(new_header_pic_stream)
        HEADER_PIC_NAME = f"{user_id}_header_pic.{new_header_pic_ext}"

        try:
            mc.put_object(
                BUCKET,
                HEADER_PIC_NAME,
                new_header_pic_stream,
                len(new_header_pic_data),
            )
            updated_header_pic = mc.presigned_get_object(BUCKET, HEADER_PIC_NAME)
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

        try:
            user.username = updated_username
            user.full_name = updated_full_name
            user.email = updated_email
            user.bio = updated_bio
            user.profile_pic = updated_profile_pic
            user.header_pic = updated_header_pic
            user.updated_at = datetime.now()

            db.session.commit()
        except:
            db.session.rollback()

            return (
                jsonify({"success": False, "message": "Failed to update the profile"}),
                500,
            )
        else:
            updated_data = user.serialize()

            return jsonify({"success": True, "data": updated_data}), 201

    return jsonify({"success": True, "data": data}), 200
