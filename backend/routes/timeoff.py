from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from extensions import db
from models import TimeOffRequest, User
from utils import role_required
from datetime import date

bp = Blueprint("timeoff", __name__, url_prefix="/api/timeoff")

@bp.route("/", methods=["GET"])
def list_timeoff():
    verify_jwt_in_request()
    claims = get_jwt()
    current_user = get_jwt_identity()
    if claims.get("role") == "manager":
        reqs = TimeOffRequest.query.all()
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
        sd = date.fromisoformat(start_date)
        ed = date.fromisoformat(end_date)
    except Exception:
        return jsonify({"msg": "invalid date format, use YYYY-MM-DD"}), 400

    if ed < sd:
        return jsonify({"msg": "end_date must be on/after start_date"}), 400

    r = TimeOffRequest(user_id=current_user, start_date=sd, end_date=ed, reason=reason)
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201

@bp.route("/<int:request_id>/status", methods=["PUT"])
@role_required("manager")
def update_status(request_id):
    r = TimeOffRequest.query.get_or_404(request_id)
    data = request.get_json() or {}
    status = data.get("status")
    if status not in ("pending", "approved", "denied"):
        return jsonify({"msg": "status must be pending|approved|denied"}), 400
    r.status = status
    db.session.commit()
    return jsonify(r.to_dict())
