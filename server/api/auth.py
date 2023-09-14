from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from flask_login import login_user, logout_user

from . import api_bp
from ..extensions import db, jwt_manager
from ..models import User, BlocklistToken


@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.execute(
        db.select(BlocklistToken).filter(BlocklistToken.jti == jti)
    ).scalar_one_or_none()

    return token is not None


@api_bp.route("/signup", methods=["POST"], strict_slashes=False)
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
                    "data": user.serialize(),
                }
            ),
            201,
        )


@api_bp.route("/signin", methods=["POST"], strict_slashes=False)
def sign_in():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user_registered = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if not user_registered or not user_registered.password_auth(
        password_input=password
    ):
        return (
            jsonify({"success": False, "message": "Username or password invalid!"}),
            400,
        )

    # If the user passes the validation process, log them in:
    # 1. Put the user into the Flask session
    login_user(user_registered)

    # 2. Give the user access and refresh token
    access_token = create_access_token(identity=user_registered.user_id)
    refresh_token = create_refresh_token(identity=user_registered.user_id)

    return (
        jsonify(
            {
                "success": True,
                "message": "Login is successful!",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        201,
    )


@api_bp.route("/signout", methods=["POST"], strict_slashes=False)
@jwt_required()
def sign_out():
    logout_user()

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
        return jsonify({"success": True, "message": "Sign out successful!"}), 200


@api_bp.route("/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()

    access_token = {"access_token": create_access_token(identity=current_user)}

    return jsonify(access_token), 201
