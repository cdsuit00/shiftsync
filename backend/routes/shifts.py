from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from extensions import db
from models import Shift, User
from utils import role_required, shift_conflict_exists
from datetime import datetime
from flask_cors import CORS

bp = Blueprint("shifts", __name__, url_prefix="/api/shifts")
# Apply CORS to this specific blueprint
CORS(bp)

@bp.route("/", methods=["GET"])
def get_shifts():
    # Skip JWT verification for OPTIONS preflight requests
    if request.method != 'OPTIONS':
        verify_jwt_in_request()
    claims = get_jwt()
    user_id = get_jwt_identity()
    if claims.get("role") == "manager":
        shifts = Shift.query.all()
    else:
        shifts = Shift.query.filter_by(user_id=user_id).all()
    return jsonify([s.to_dict() for s in shifts])

@bp.route("/", methods=["POST"])
@role_required("manager")
def create_shift():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    title = data.get("title")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    notes = data.get("notes")

    if not (user_id and title and start_time and end_time):
        return jsonify({"msg": "user_id, title, start_time, end_time required"}), 400

    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except Exception:
        return jsonify({"msg": "invalid datetime format, use ISO 8601"}), 400

    if end_dt <= start_dt:
        return jsonify({"msg": "end_time must be after start_time"}), 400

    if not User.query.get(user_id):
        return jsonify({"msg": "user not found"}), 404

    if shift_conflict_exists(user_id, start_dt, end_dt):
        return jsonify({"msg": "shift conflict detected for user"}), 409

    s = Shift(user_id=user_id, title=title, start_time=start_dt, end_time=end_dt, notes=notes)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@bp.route("/<int:shift_id>", methods=["PUT"])
@role_required("manager")
def update_shift(shift_id):
    s = Shift.query.get_or_404(shift_id)
    data = request.get_json() or {}
    user_id = data.get("user_id", s.user_id)
    title = data.get("title", s.title)
    start_time = data.get("start_time", s.start_time.isoformat())
    end_time = data.get("end_time", s.end_time.isoformat())
    notes = data.get("notes", s.notes)

    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except Exception:
        return jsonify({"msg": "invalid datetime format"}), 400

    if end_dt <= start_dt:
        return jsonify({"msg": "end_time must be after start_time"}), 400

    if shift_conflict_exists(user_id, start_dt, end_dt, exclude_shift_id=shift_id):
        return jsonify({"msg": "shift conflict detected for user"}), 409

    s.user_id = user_id
    s.title = title
    s.start_time = start_dt
    s.end_time = end_dt
    s.notes = notes
    db.session.commit()
    return jsonify(s.to_dict())

@bp.route("/<int:shift_id>", methods=["DELETE"])
@role_required("manager")
def delete_shift(shift_id):
    s = Shift.query.get_or_404(shift_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"msg": "deleted"}), 200
