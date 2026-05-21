# Secure Document Vault - Final Project

## Features Implemented (All Requirements Covered)
- User Registration + Login with Password Policy
- bcrypt Password Hashing
- JWT Authentication
- 2FA (TOTP)
- RBAC: Admin, Manager, User
- Document Upload, Download, Delete
- AES-GCM Encryption (user password)
- RSA Digital Signature + SHA-256 Hash
- Integrity Verification
- HTTPS Support
- Complete Web UI (Bootstrap)

## How to Run

```bash
pip install -r requirements.txt

# Database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

python run.py