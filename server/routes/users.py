from flask import request, jsonify
from flask_jwt_extended import jwt_required
from minio.error import S3Error
from datetime import datetime
import base64
import io
import imghdr

from . import routes
from ..extensions import db, mc
from ..models import User

BUCKET = "xweeter"


@routes.route("/users", methods=["GET"], strict_slashes=False)
# @jwt_required()
def get_users():
    users = db.session.execute(db.select(User)).scalars()
    data = [user.serialize() for user in users]

    return jsonify({"success": True, "data": data}), 200


@routes.route("/users/<int:user_id>", methods=["GET", "PUT"], strict_slashes=False)
# @jwt_required()
def access_user(user_id):
    user = db.session.execute(
        db.select(User).filter(User.user_id == user_id)
    ).scalar_one_or_none()
    data = user.serialize()

    if request.method == "PUT":
        updated_data = request.get_json()
        # updated_username = updated_data.get("username")
        # updated_full_name = updated_data.get("fullname")
        # updated_email = updated_data.get("email")
        # updated_bio = updated_data.get("bio")
        updated_profile_pic = updated_data.get("profile_pic")
        # updated_header_pic = updated_data.get("header_pic")

        if updated_profile_pic:
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

            # new_header_pic_data = base64.b64decode(updated_header_pic.split(",")[1])
            # new_header_pic_stream = io.BytesIO(new_header_pic_data)
            # new_header_pic_ext = imghdr.what(new_header_pic_stream)
            # HEADER_PIC_NAME = f"{user_id}_header_pic.{new_header_pic_ext}"

        try:
            # user.username = updated_username
            # user.full_name = updated_full_name
            # user.email = updated_email
            # user.bio = updated_bio
            user.profile_pic = updated_profile_pic
            # user.header_pic = updated_header_pic
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
