from flask import Blueprint, jsonify
from models import User
from utils import role_required
from flask_jwt_extended import verify_jwt_in_request
from flask_cors import CORS

bp = Blueprint("users", __name__, url_prefix="/api/users")
CORS(bp)


@bp.route("/", methods=["GET"])
@role_required("manager")
def list_users():
    # managers can get a list of users to assign shifts
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])
