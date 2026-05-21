from flask import Blueprint, render_template, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Document
from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
@role_required('Admin')
def manage_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/all-documents')
@role_required('Admin', 'Manager')
def all_documents():
    docs = Document.query.all()
    return render_template('admin_documents.html', documents=docs)