import re
from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from flask_cors import CORS
import bleach  # Add to requirements.txt

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
# Enable CORS specifically for this blueprint
CORS(bp, supports_credentials=True)

def validate_password(password):
    """Enforce password strength requirements"""
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return "Password must contain at least one number"
    return None

@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = bleach.clean(data.get("username", "").strip())
    email = bleach.clean(data.get("email", "").strip().lower())
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"msg": "username, email and password required"}), 400
    
    # Validate email format
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return jsonify({"msg": "Invalid email format"}), 400
    
    # Validate password strength
    password_error = validate_password(password)
    if password_error:
        return jsonify({"msg": password_error}), 400
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"msg": "username or email already exists"}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"msg": "user created"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username_or_email = bleach.clean(data.get("username") or data.get("email", ""))
    password = data.get("password")
    
    if not username_or_email or not password:
        return jsonify({"msg": "username/email and password required"}), 400
    
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username/email or password"}), 401
    
    additional_claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(
        identity=user.id, 
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@bp.route("/refresh", methods=["POST"])
def refresh():
    from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    additional_claims = {"role": user.role, "username": user.username}
    new_token = create_access_token(
        identity=current_user, 
        additional_claims=additional_claims
    )
    return jsonify({"access_token": new_token}), 200