from flask import request, jsonify

from . import api_bp
from ..extensions import db
from ..models import Users


@api_bp.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    users = db.session.execute(db.select(Users)).scalars()
    data = [user.serialize() for user in users]

    return jsonify({"success": True, "data": data}), 200


@api_bp.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
def access_user(user_id):
    user = db.session.execute(
        db.select(Users).filter_by(user_id=user_id)
    ).scalar_one_or_none()
    data = user.serialize()

    return jsonify({"success": True, "data": data}), 200
