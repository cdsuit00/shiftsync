from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from datetime import datetime, date, timedelta
from models import Shift
from extensions import db

def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Skip JWT verification for OPTIONS requests
            if request.method != 'OPTIONS':
                verify_jwt_in_request()
                claims = get_jwt()
                if claims.get("role") != role_name:
                    return jsonify({"msg": "Forbidden - manager only"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def roles_allowed(*role_names):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in role_names:
                return jsonify({"msg": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def shift_conflict_exists(user_id, start_dt, end_dt, exclude_shift_id=None):
    # conflict if existing.start < new_end and existing.end > new_start
    query = Shift.query.filter(
        Shift.user_id == user_id,
        Shift.start_time < end_dt,
        Shift.end_time > start_dt
    )
    if exclude_shift_id:
        query = query.filter(Shift.id != exclude_shift_id)
    return query.first() is not None
