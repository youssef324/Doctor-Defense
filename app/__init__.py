import os

from flask import Flask, g, redirect, request, url_for
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
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

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
