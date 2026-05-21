from io import BytesIO
import os

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename

from app.models import Document, User, db
from app.utils.crypto import decrypt_file, encrypt_file, sign_document, verify_signature
from app.utils.decorators import twofa_setup_required

documents_bp = Blueprint('documents', __name__)


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )


def _get_current_user():
    user_id = int(get_jwt_identity())
    return db.session.get(User, user_id)


def _can_access_document(doc, user):
    if doc.user_id == user.id:
        return True
    return user.role in ('Admin', 'Manager')


@documents_bp.route('/dashboard')
@twofa_setup_required
def dashboard():
    user = _get_current_user()
    if not user:
        abort(401)

    documents = Document.query.filter_by(user_id=user.id).all()
    twofa_enabled = bool(user.totp_secret)

    show_2fa_complete = session.pop('show_2fa_complete', False)

    return render_template(
        'dashboard.html',
        user=user,
        documents=documents,
        twofa_enabled=twofa_enabled,
        show_2fa_complete=show_2fa_complete,
    )


@documents_bp.route('/upload', methods=['GET', 'POST'])
@twofa_setup_required
def upload():
    if request.method == 'POST':
        if 'files' not in request.files:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "No files selected"}), 400
            flash('No files selected', 'danger')
            return redirect(url_for('documents.upload'))

        files = request.files.getlist('files')
        password = request.form.get('password')

        if not files or files[0].filename == '':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "No files selected"}), 400
            flash('No files selected', 'danger')
            return redirect(url_for('documents.upload'))

        if not password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Password is required for encryption"}), 400
            flash('Password is required for encryption', 'danger')
            return redirect(url_for('documents.upload'))

        user = _get_current_user()
        uploaded_count = 0

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_data = file.read()

                encrypted_data = encrypt_file(file_data, password)
                signature, file_hash = sign_document(file_data)

                enc_filename = f"{os.urandom(16).hex()}_{filename}"
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], enc_filename)

                with open(save_path, 'wb') as f:
                    f.write(encrypted_data)

                doc = Document(
                    original_filename=filename,
                    encrypted_filename=enc_filename,
                    user_id=user.id,
                    file_hash=file_hash,
                    signature=signature,
                    size=len(file_data),
                    mime_type=file.mimetype,
                )
                db.session.add(doc)
                uploaded_count += 1

        db.session.commit()
        message = f'Successfully uploaded and encrypted {uploaded_count} file(s)!'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": message})

        flash(message, 'success')
        return redirect(url_for('documents.dashboard'))

    return render_template('upload.html')


@documents_bp.route('/download/<int:doc_id>', methods=['POST'])
@twofa_setup_required
def download(doc_id):
    user = _get_current_user()
    doc = Document.query.get_or_404(doc_id)

    if doc.user_id != user.id:
        abort(403)

    password = request.form.get('password')
    if not password:
        flash('Password is required to decrypt the file', 'danger')
        return redirect(url_for('documents.dashboard'))

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.encrypted_filename)

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    try:
        decrypted_data = decrypt_file(encrypted_data, password)
        if not verify_signature(decrypted_data, doc.signature):
            flash('Integrity check failed. The document may have been tampered with.', 'danger')
            return redirect(url_for('documents.dashboard'))

        return send_file(
            BytesIO(decrypted_data),
            as_attachment=True,
            download_name=doc.original_filename,
        )
    except Exception:
        flash('Decryption failed. Check your password and try again.', 'danger')
        return redirect(url_for('documents.dashboard'))


@documents_bp.route('/verify/<int:doc_id>', methods=['GET', 'POST'])
@twofa_setup_required
def verify(doc_id):
    user = _get_current_user()
    doc = Document.query.get_or_404(doc_id)

    if not _can_access_document(doc, user):
        abort(403)

    verified = None
    error = None

    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            error = 'Password is required to verify the document.'
        else:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.encrypted_filename)
            try:
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = decrypt_file(encrypted_data, password)
                verified = verify_signature(decrypted_data, doc.signature)
                if not verified:
                    error = 'Signature verification failed. The file may have been modified.'
            except Exception:
                error = 'Verification failed. Wrong password or corrupted file.'

    return render_template('verify.html', doc=doc, verified=verified, error=error)


@documents_bp.route('/delete/<int:doc_id>', methods=['POST'])
@twofa_setup_required
def delete_document(doc_id):
    user = _get_current_user()
    doc = Document.query.get_or_404(doc_id)

    if doc.user_id != user.id and user.role != 'Admin':
        abort(403)

    password = request.form.get('password')
    if doc.user_id == user.id:
        if not password:
            flash('Password is required to delete the file', 'danger')
            return redirect(url_for('documents.dashboard'))

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.encrypted_filename)
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            _ = decrypt_file(encrypted_data, password)
        except Exception:
            flash('Password incorrect. Document not deleted.', 'danger')
            return redirect(url_for('documents.dashboard'))

    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.encrypted_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(doc)
        db.session.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"message": "Document deleted successfully"})

        flash('Document deleted successfully', 'success')
    except Exception:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"error": "Failed to delete document"}), 500
        flash('Failed to delete document', 'danger')

    return redirect(url_for('documents.dashboard'))
