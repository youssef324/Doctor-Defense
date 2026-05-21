# pyrefly: ignore [missing-import]
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
# pyrefly: ignore [missing-import]
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

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@role_required('Admin')
def modify_user_role(user_id):
    current_user_id = int(get_jwt_identity())
    
    if current_user_id == user_id:
        flash('You cannot modify your own role.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')

    if new_role not in ['Admin', 'Manager', 'User']:
        flash('Invalid role selected.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user.role = new_role
    from app.models import db
    db.session.commit()
    
    flash(f"User {user.username}'s role has been updated to {new_role}.", 'success')
    return redirect(url_for('admin.manage_users'))