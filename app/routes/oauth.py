import os
from flask import Blueprint, redirect, url_for, flash
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import create_access_token, set_access_cookies
from app.models import User, db

oauth_bp = Blueprint('oauth', __name__)
oauth = OAuth()

google = None
github = None


def register_oauth_providers(app):
    global google, github

    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    github = oauth.register(
        name='github',
        client_id=app.config['GITHUB_CLIENT_ID'],
        client_secret=app.config['GITHUB_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )


@oauth_bp.route('/google')
def google_login():
    if not google:
        flash("Google OAuth is not configured", "danger")
        return redirect(url_for('auth.login'))
    redirect_uri = url_for('oauth.google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@oauth_bp.route('/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        user_info = google.get('https://openidconnect.googleapis.com/v1/userinfo').json()
        return _handle_oauth_user(
            user_info['email'],
            user_info.get('name', user_info['email'].split('@')[0]),
            'Google'
        )
    except Exception as e:
        flash(f"Google login failed: {str(e)}", "danger")
        return redirect(url_for('auth.login'))


@oauth_bp.route('/github')
def github_login():
    if not github:
        flash("GitHub OAuth is not configured", "danger")
        return redirect(url_for('auth.login'))
    redirect_uri = url_for('oauth.github_callback', _external=True)
    return github.authorize_redirect(redirect_uri)


@oauth_bp.route('/github/callback')
def github_callback():
    try:
        token = github.authorize_access_token()
        user_info = github.get('user').json()
        emails = github.get('user/emails').json()
        email = next((e['email'] for e in emails if e.get('primary')), None)

        if not email:
            flash("Could not retrieve email from GitHub", "danger")
            return redirect(url_for('auth.login'))

        return _handle_oauth_user(email, user_info['login'], 'GitHub')
    except Exception as e:
        flash(f"GitHub login failed: {str(e)}", "danger")
        return redirect(url_for('auth.login'))


def _handle_oauth_user(email, username, provider):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=username, email=email, role='User')
        user.set_password(os.urandom(32).hex())  # Random secure password
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    response = redirect(url_for('documents.dashboard'))
    set_access_cookies(response, access_token)
    flash(f'Welcome! Logged in successfully with {provider}.', 'success')
    return response