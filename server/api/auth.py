from flask import request, jsonify

from . import api_bp

from ..extensions import db
from ..models import Users


@api_bp.route("/signup", methods=["POST"], strict_slashes=False)
def sign_up():
    data = request.get_json()
    username = data["username"]
    full_name = data["fullname"]
    email = data["email"]
    password = data["password"]

    user = Users(username=username, full_name=full_name, email=email, password=password)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()

        return (
            jsonify({"success": False, "message": "Failed to register the user"}),
            500,
        )
    else:
        return (
            jsonify(
                {
                    "success": True,
                    "message": "User registration is completed",
                    "data": user.serialize(),
                }
            ),
            201,
        )
