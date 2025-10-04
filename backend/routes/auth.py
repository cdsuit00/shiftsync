from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "username, email and password required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "username or email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    # default role = employee
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "user created"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username_or_email = data.get("username") or data.get("email")
    password = data.get("password")

    if not username_or_email or not password:
        return jsonify({"msg": "username/email and password required"}), 400

    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username/email or password"}), 401

    additional_claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200
