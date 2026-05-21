from io import BytesIO
import base64

import pyotp
import qrcode
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from app.models import User, db

auth_bp = Blueprint('auth', __name__)

PENDING_TOTP_KEY = 'pending_totp_secret'


def _pending_totp_secret():
    return session.get(PENDING_TOTP_KEY)


def _set_pending_totp_secret(secret):
    session[PENDING_TOTP_KEY] = secret


def _clear_pending_totp_secret():
    session.pop(PENDING_TOTP_KEY, None)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', 'User')

        if role not in ('User', 'Manager', 'Admin'):
            role = 'User'

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists', 'danger')
            return redirect(url_for('auth.register'))

        if password != password_confirm:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            flash('Password must be at least 8 characters with uppercase letter and number', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Account created! Log in next, then complete the quick 2FA setup.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    requires_2fa = False
    username_value = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        totp_code = request.form.get('totp_code', '').strip()
        username_value = username

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.totp_secret:
                requires_2fa = True
                totp = pyotp.TOTP(user.totp_secret)
                if not totp_code or not totp.verify(totp_code, valid_window=1):
                    flash('Enter the 6-digit code from your authenticator app.', 'danger')
                    return render_template(
                        'login.html',
                        requires_2fa=True,
                        username_value=username_value,
                    )

            access_token = create_access_token(identity=str(user.id))
            if user.totp_secret:
                response = redirect(url_for('documents.dashboard'))
                flash('Welcome back!', 'success')
            else:
                response = redirect(url_for('auth.setup_2fa'))
                flash('Step 2: Set up two-factor authentication to secure your vault.', 'info')
            set_access_cookies(response, access_token)
            return response

        flash('Invalid username or password', 'danger')

    return render_template(
        'login.html',
        requires_2fa=requires_2fa,
        username_value=username_value,
    )


@auth_bp.route('/2fa-setup', methods=['GET', 'POST'])
@jwt_required()
def setup_2fa():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))

    already_enabled = bool(user.totp_secret)

    if request.method == 'POST' and not already_enabled:
        code = request.form.get('totp_code', '').strip()
        secret = _pending_totp_secret()

        if not secret:
            flash('Setup session expired. Please refresh this page.', 'warning')
            return redirect(url_for('auth.setup_2fa'))

        totp = pyotp.TOTP(secret)
        if not code or not totp.verify(code, valid_window=1):
            flash('Invalid code. Open your authenticator app and try again.', 'danger')
            return _render_2fa_setup(user, secret, step=3)

        user.totp_secret = secret
        db.session.commit()
        _clear_pending_totp_secret()
        session['show_2fa_complete'] = True

        flash('2FA enabled! Log out, then sign in again with your 6-digit code.', 'success')
        return redirect(url_for('documents.dashboard'))

    if already_enabled:
        secret = user.totp_secret
        step = 4
    else:
        secret = _pending_totp_secret() or pyotp.random_base32()
        _set_pending_totp_secret(secret)
        step = 2 if request.method == 'GET' else 3

    return _render_2fa_setup(user, secret, step=step, already_enabled=already_enabled)


def _render_2fa_setup(user, secret, step=2, already_enabled=False):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.email, issuer_name='SecureDocumentVault')

    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format='PNG')
    qr_code = base64.b64encode(buffered.getvalue()).decode()

    return render_template(
        '2fa_setup.html',
        qr_code=qr_code,
        secret=secret,
        user=user,
        step=step,
        already_enabled=already_enabled,
    )


@auth_bp.route('/logout')
def logout():
    _clear_pending_totp_secret()
    session.pop('show_2fa_complete', None)
    response = redirect(url_for('auth.login'))
    unset_jwt_cookies(response)
    response.delete_cookie('jwt_token')
    flash('Logged out. Sign in again with your password and 6-digit 2FA code.', 'info')
    return response
