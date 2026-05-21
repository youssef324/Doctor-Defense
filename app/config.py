import os
from datetime import timedelta
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load .env file
load_dotenv()

_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_INSTANCE_DIR = os.path.join(_BASE_DIR, 'instance')
_UPLOAD_DIR = os.path.join(_BASE_DIR, 'uploads')

os.makedirs(_INSTANCE_DIR, exist_ok=True)
os.makedirs(_UPLOAD_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(_INSTANCE_DIR, 'vault.db').replace('\\', '/')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_TOKEN_LOCATION = ['cookies']
    
    # Security: Use environment variable to control HTTPS requirement
    # In production, set FLASK_ENV=production to enforce HTTPS
    _IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production'
    JWT_COOKIE_SECURE = _IS_PRODUCTION or os.environ.get('JWT_COOKIE_SECURE', 'False').lower() == 'true'
    JWT_COOKIE_CSRF_PROTECT = True  # Enable CSRF protection for JWT cookies
    JWT_ACCESS_COOKIE_NAME = 'jwt_token'
    JWT_COOKIE_SAMESITE = 'Strict'  # Changed from 'Lax' to 'Strict' for better security
    JWT_COOKIE_HTTPONLY = True  # Prevent JavaScript access to cookies

    # === OAuth Config ===
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

    UPLOAD_FOLDER = _UPLOAD_DIR
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'png', 'zip', 'rar'}

    INSTANCE_PATH = _INSTANCE_DIR
