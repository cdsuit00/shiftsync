from flask import Blueprint, jsonify
from flask_jwt_extended import verify_jwt_in_request
from datetime import date, datetime, timedelta
from models import Shift

bp = Blueprint("schedules", __name__, url_prefix="/api/schedules")

@bp.route("/<string:week_start>", methods=["GET"])
def week_schedule(week_start):
    """
    week_start should be YYYY-MM-DD (a date representing the week's Monday or any day in week).
    Returns all shifts whose start_time is within that 7-day window.
    """
    verify_jwt_in_request()
    try:
        start_date = date.fromisoformat(week_start)
    except Exception:
        return jsonify({"msg": "invalid date format for week_start, use YYYY-MM-DD"}), 400

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = start_dt + timedelta(days=7)
    shifts = Shift.query.filter(Shift.start_time >= start_dt, Shift.start_time < end_dt).all()
    return jsonify([s.to_dict() for s in shifts])
