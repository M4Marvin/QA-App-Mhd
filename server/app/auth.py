from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User
from app import db


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = db.session.get(User, current_user_id)
            if user.role not in allowed_roles:
                return jsonify({"message": "Access denied!"}), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator
