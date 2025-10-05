from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from extensions import db
from models import TimeOffRequest, User, Shift
from utils import role_required
from datetime import date, datetime
from sqlalchemy import and_
from flask_cors import CORS

bp = Blueprint("timeoff", __name__, url_prefix="/api/timeoff")
CORS(bp)

def has_shift_conflict(user_id, start_date, end_date):
    """Check if time-off request conflicts with existing shifts"""
    conflicts = Shift.query.filter(
        Shift.user_id == user_id,
        and_(
            Shift.start_time.date() <= end_date,
            Shift.end_time.date() >= start_date
        )
    ).first()
    return conflicts is not None

@bp.route("/", methods=["GET"])
def list_timeoff():
    verify_jwt_in_request()
    claims = get_jwt()
    current_user = get_jwt_identity()
    
    if claims.get("role") == "manager":
        reqs = TimeOffRequest.query.join(User).all()
        result = []
        for r in reqs:
            data = r.to_dict()
            data["user_name"] = r.user.username
            result.append(data)
        return jsonify(result)
    else:
        reqs = TimeOffRequest.query.filter_by(user_id=current_user).all()
        return jsonify([r.to_dict() for r in reqs])

@bp.route("/", methods=["POST"])
def create_timeoff():
    verify_jwt_in_request()
    current_user = get_jwt_identity()
    data = request.get_json() or {}
    
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    reason = data.get("reason", "")

    try:
        sd = date.fromisoformat(start_date)  # Expects YYYY-MM-DD
        ed = date.fromisoformat(end_date)    # Expects YYYY-MM-DD
    except Exception:
        return jsonify({"msg": "invalid date format, use YYYY-MM-DD"}), 400

    if ed < sd:
        return jsonify({"msg": "end_date must be on/after start_date"}), 400
    
    # Check for shift conflicts
    if has_shift_conflict(current_user, sd, ed):
        return jsonify({"msg": "Time-off request conflicts with existing shifts"}), 409
    
    r = TimeOffRequest(user_id=current_user, start_date=sd, end_date=ed, reason=reason)
    db.session.add(r)
    db.session.commit()
    
    return jsonify(r.to_dict()), 201

@bp.route("/<int:request_id>", methods=["DELETE"])
def delete_timeoff(request_id):
    verify_jwt_in_request()
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    r = TimeOffRequest.query.get_or_404(request_id)
    
    # Users can delete their own pending requests, managers can delete any
    if r.user_id != current_user and claims.get("role") != "manager":
        return jsonify({"msg": "Forbidden"}), 403
    
    if r.status != "pending" and claims.get("role") != "manager":
        return jsonify({"msg": "Can only delete pending requests"}), 400
    
    db.session.delete(r)
    db.session.commit()
    return jsonify({"msg": "deleted"}), 200