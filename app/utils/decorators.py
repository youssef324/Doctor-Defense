from functools import wraps

# pyrefly: ignore [missing-import]
from flask import abort, redirect, url_for, flash
# pyrefly: ignore [missing-import]
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import User, db


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = int(get_jwt_identity())
            user = db.session.get(User, user_id)
            if not user or user.role not in roles:
                abort(403, description='Access denied')
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def twofa_setup_required(f):
    """Redirect to 2FA setup until the user has confirmed two-factor authentication."""

    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)
        if not user:
            abort(401)
        if not user.totp_secret:
            flash('Set up two-factor authentication to access your vault.', 'warning')
            return redirect(url_for('auth.setup_2fa'))
        return f(*args, **kwargs)

    return decorated_function
