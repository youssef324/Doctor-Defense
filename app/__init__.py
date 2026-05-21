from urllib import response
import os

# pyrefly: ignore [missing-import]
from flask import Flask, g, redirect, request, url_for
# pyrefly: ignore [missing-import]
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
# pyrefly: ignore [missing-import]
from flask_migrate import Migrate

from app.config import Config
from app.models import User, bcrypt, db
from app.routes.oauth import oauth_bp, oauth
from app.utils.crypto import init_keys

jwt = JWTManager()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    if app.config.get('JWT_COOKIE_SECURE'):
        @app.before_request
        def enforce_https():
            if not request.is_secure and not app.debug:
                url = request.url.replace('http://', 'https://', 1)
                return redirect(url, code=301)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    from app.routes.oauth import register_oauth_providers
    register_oauth_providers(app)

    os.makedirs(app.config['INSTANCE_PATH'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    init_keys(app.config['INSTANCE_PATH'])

    from app.routes.auth import auth_bp
    from app.routes.documents import documents_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(documents_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(oauth_bp, url_prefix='/oauth')

    @app.context_processor
    def inject_current_user():
        return {'current_user': g.get('current_user')}

    @app.before_request
    def load_user_from_jwt():
        g.current_user = None
        if request.endpoint and request.endpoint.startswith('static'):
            return
        try:
            verify_jwt_in_request(optional=True, locations=['cookies'])
            user_id = get_jwt_identity()
            if user_id is not None:
                g.current_user = db.session.get(User, int(user_id))
        except Exception:
            g.current_user = None

    @app.before_request
    def enforce_https():
        """Enforce HTTPS in production to protect against MITM attacks."""
        if app.config['JWT_COOKIE_SECURE'] and not request.is_secure and not app.debug:
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)

    @app.after_request
    def set_security_headers(response):
        """Add security headers to protect against common attacks."""
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; font-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net"
        return response

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    @app.after_request
    def set_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
    return app
