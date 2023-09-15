from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies,
)
from datetime import datetime, timezone, timedelta
import logging

from . import routes
from ..extensions import db, jwt_manager
from ..models import User, BlocklistToken

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.execute(
        db.select(BlocklistToken).filter(BlocklistToken.jti == jti)
    ).scalar_one_or_none()

    return token is not None


@routes.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))

        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)

        return response
    except (RuntimeError, KeyError):
        return response


@routes.route("/signup", methods=["POST"], strict_slashes=False)
def sign_up():
    data = request.get_json()
    username = data["username"]
    full_name = data["fullname"]
    email = data["email"]
    password = data["password"]

    user = User(username=username, full_name=full_name, email=email, password=password)

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
                    "user": user.serialize(),
                }
            ),
            201,
        )


@routes.route("/signin", methods=["POST"], strict_slashes=False)
def sign_in():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    registered_user = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if not registered_user or not registered_user.password_auth(
        password_input=password
    ):
        error_msg = "Username or password invalid!"
        logging.error(
            f"Failed login attempt for username: {username}, Error: {error_msg}"
        )

        return (
            jsonify({"success": False, "message": error_msg}),
            400,
        )

    access_token = create_access_token(identity=registered_user.user_id)

    response = jsonify(
        {
            "success": True,
            "message": "Login is successful!",
            "user": registered_user.serialize(),
        }
    )
    set_access_cookies(response, access_token)

    return response, 201


@routes.route("/signout", methods=["POST"], strict_slashes=False)
@jwt_required()
def sign_out():
    jwt = get_jwt()
    jti = jwt.get("jti")

    token = BlocklistToken(jti=jti)

    try:
        db.session.add(token)
        db.session.commit()
    except:
        db.session.rollback()

        return jsonify({"success": False, "message": "Failed to sign out"}), 500
    else:
        response = jsonify({"success": True, "message": "Sign out successful!"})
        unset_jwt_cookies(response)

        return response, 200
