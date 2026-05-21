<!-- README.md for Doctor-Defense Project -->
<div align="center">
  <h1>🏥 Doctor-Defense: Secure Document Vault System</h1>
  <p>
    <strong>A modern, enterprise-grade secure document management platform with end-to-end encryption, digital signatures, and role-based access control.</strong>
  </p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
  [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-red?style=flat-square&logo=database)](https://www.sqlalchemy.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](#)

  [Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Security](#-security) • [Deployment](#-deployment)
</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [👥 User Roles & Permissions](#-user-roles--permissions)
- [🔧 Development Stack](#-development-stack)
- [💾 Database Schema](#-database-schema)
- [🚀 Installation & Setup](#-installation--setup)
- [📖 Usage Guide](#-usage-guide)
- [🔐 Security Features](#-security-features)
- [🌐 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📚 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

**Doctor-Defense** is a secure, enterprise-grade document management system designed to protect sensitive information with military-grade encryption, digital signatures, and comprehensive access controls. Built with modern security practices, it ensures documents are encrypted at rest, authenticated with digital signatures, and accessible only to authorized users.

### Key Highlights
- 🔐 **AES-256-GCM** encryption for stored documents
- 🖊️ **RSA-2048** digital signatures for document integrity
- 🔑 **Mandatory 2FA** for all users
- 👥 **Role-Based Access Control** (Admin, Manager, User)
- 🔓 **OAuth 2.0** integration (Google & GitHub)
- 🌐 **HTTPS enforcement** with security headers
- 📊 **Beautiful responsive UI** with real-time feedback

---

## ✨ Features

### 🔐 Security Features
- ✅ **End-to-End Encryption** - AES-256-GCM encryption with secure key derivation (Scrypt)
- ✅ **Digital Signatures** - RSA-2048 signatures with SHA-256 hashing
- ✅ **Two-Factor Authentication** - TOTP-based 2FA with QR code setup
- ✅ **Password Security** - Bcrypt hashing with enforced password policy
- ✅ **OAuth 2.0** - GitHub and Google OAuth login support
- ✅ **HTTPS Enforcement** - Automatic redirect with HSTS headers
- ✅ **Security Headers** - CSP, X-Frame-Options, X-XSS-Protection
- ✅ **CSRF Protection** - JWT-based CSRF tokens in cookies

### 📁 Document Management
- ✅ **Multi-file Upload** - Drag-and-drop upload with progress tracking
- ✅ **Encryption on Upload** - Automatic AES-256 encryption before storage
- ✅ **Integrity Verification** - Digital signature verification on download
- ✅ **File Metadata** - Size, type, upload timestamp, and owner tracking
- ✅ **Document Sharing** - Role-based access for Admin/Manager users
- ✅ **File Type Validation** - Supported: PDF, DOC, DOCX, TXT, JPG, PNG, ZIP, RAR
- ✅ **Size Limits** - Maximum 50MB per file

### 👥 User Management
- ✅ **User Registration** - Self-service registration with password policy
- ✅ **Role Assignment** - Three-tier role system (Admin, Manager, User)
- ✅ **Admin Panel** - User and role management interface
- ✅ **Session Management** - JWT tokens with automatic expiration (2 hours)
- ✅ **Activity Tracking** - Document access and modification logs

### 🎨 User Experience
- ✅ **Responsive Design** - Mobile-first design with Bootstrap 5
- ✅ **Real-time Feedback** - Toast notifications and error handling
- ✅ **AJAX Upload** - Non-blocking file uploads with progress bars
- ✅ **Dark Theme** - Professional dark UI with accent colors
- ✅ **Intuitive Navigation** - Easy-to-use dashboard and controls

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (UI Layer)                       │
│  ┌──────────────────┬──────────────────┬──────────────────┐    │
│  │  Dashboard      │  Upload Portal   │  Admin Panel     │    │
│  │  HTML/CSS/JS    │  HTML/CSS/JS     │  HTML/CSS/JS     │    │
│  └──────────────────┴──────────────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ▼ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                     Backend API Layer (Flask)                    │
│  ┌────────────────┬──────────────────┬──────────────────┐      │
│  │  Auth Routes   │  Document Routes │  Admin Routes    │      │
│  │  /auth/login   │  /upload         │  /admin/users    │      │
│  │  /auth/2fa     │  /download       │  /admin/docs     │      │
│  │  /oauth/*      │  /verify         │  /admin/roles    │      │
│  └────────────────┴──────────────────┴──────────────────┘      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────┐       │
│  │           Security & Middleware Layer                │       │
│  │  JWT Verification • HTTPS Redirect • CSRF Protection │       │
│  │  Security Headers • Rate Limiting • Access Control   │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Cryptography Layer                              │
│  ┌──────────────────┬──────────────────┬─────────────────┐    │
│  │ AES-256-GCM      │ RSA-2048         │ Bcrypt          │    │
│  │ Encryption       │ Digital Sig      │ Password Hash   │    │
│  └──────────────────┴──────────────────┴─────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Database Layer                                │
│  ┌──────────────────┬──────────────────┬─────────────────┐    │
│  │ SQLite (Dev)     │ PostgreSQL (Prod)│ Encrypted Files │    │
│  │ User Table       │ Document Table   │ Key Storage     │    │
│  └──────────────────┴──────────────────┴─────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 User Roles & Permissions

### 🔑 Three-Tier Role System

| Feature | Admin | Manager | User |
|---------|-------|---------|------|
| **Manage Users** | ✅ | ❌ | ❌ |
| **Modify Roles** | ✅ | ❌ | ❌ |
| **View All Documents** | ✅ | ✅ | ❌ |
| **Verify Documents** | ✅ | ✅ | ❌ |
| **Upload Documents** | ✅ | ✅ | ✅ |
| **Download Own Documents** | ✅ | ✅ | ✅ |
| **Delete Own Documents** | ✅ | ✅ | ✅ |
| **Access Admin Panel** | ✅ | ❌ | ❌ |
| **View Dashboard** | ✅ | ✅ | ✅ |

### Permission Details

#### **Admin** 👨‍💼
- Full system access
- Manage all users and roles
- View all documents across the platform
- Verify document integrity
- Access admin control panel
- Generate reports

#### **Manager** 👨‍📋
- Review and verify documents
- View all documents
- Upload and manage own documents
- Assist with document approval workflow
- Cannot modify user roles or access admin panel

#### **User** 👤
- Upload and encrypt documents
- Download and decrypt own documents
- Delete own documents
- Verify integrity of own documents
- Access personal dashboard

---

## 🔧 Development Stack

### **Backend**

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Flask | 2.0+ | Web application framework |
| **Database ORM** | SQLAlchemy | 1.4+ | Database abstraction layer |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) | 3.x / 13+ | Data persistence |
| **Authentication** | Flask-JWT-Extended | 4.0+ | JWT token management |
| **Password Hashing** | Flask-Bcrypt | 1.0+ | Secure password storage |
| **2FA** | PyOTP | 2.6+ | TOTP implementation |
| **OAuth** | Authlib | 1.0+ | OAuth 2.0 integration |
| **Encryption** | Cryptography | 36.0+ | AES-256 & RSA cryptography |
| **Migrations** | Flask-Migrate | 3.0+ | Database schema management |

### **Frontend**

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Bootstrap | 5.x | Responsive CSS framework |
| **Icons** | Font Awesome | 6.x | Icon library |
| **Charts** | Chart.js | 3.x | Data visualization |
| **QR Codes** | QRCode | 7.x | 2FA QR generation |
| **AJAX** | Vanilla JS | - | Asynchronous requests |
| **File Upload** | Dropzone.js | 5.x | Drag-and-drop upload |

### **Development Tools**

| Tool | Purpose |
|------|---------|
| **Python 3.8+** | Runtime environment |
| **pip** | Python package manager |
| **Virtual Environment** | Isolated Python environment |
| **Git** | Version control |
| **GitHub** | Repository hosting |
| **VS Code / PyCharm** | IDE |
| **Postman** | API testing (optional) |
| **Wireshark** | Network traffic analysis |

### **Production Tools**

| Tool | Purpose |
|------|---------|
| **Gunicorn / Waitress** | WSGI application server |
| **Nginx** | Reverse proxy & SSL termination |
| **Let's Encrypt** | Free SSL certificates |
| **Docker** | Containerization |
| **PostgreSQL** | Production database |
| **Supervisor** | Process management |

---

## 💾 Database Schema

### **User Table**
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'User',  -- Admin, Manager, User
    totp_secret VARCHAR(32),           -- 2FA secret
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Document Table**
```sql
CREATE TABLE document (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename VARCHAR(255) NOT NULL,
    encrypted_filename VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL FOREIGN KEY,
    file_hash VARCHAR(64) NOT NULL,    -- SHA-256 hash
    signature TEXT NOT NULL,            -- RSA signature (hex)
    size INTEGER NOT NULL,              -- File size in bytes
    mime_type VARCHAR(100),             -- Content type
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Entity Relationship Diagram**
```
┌──────────────────┐
│     User         │
├──────────────────┤
│ id (PK)          │
│ username (UQ)    │
│ email (UQ)       │
│ password_hash    │
│ role             │
│ totp_secret      │
│ created_at       │
└──────────────────┘
         │
         │ 1:M
         │
         ▼
┌──────────────────┐
│   Document       │
├──────────────────┤
│ id (PK)          │
│ original_filename│
│ encrypted_file   │
│ user_id (FK)     │
│ file_hash        │
│ signature        │
│ size             │
│ mime_type        │
│ uploaded_at      │
└──────────────────┘
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)
- Virtual environment support
- Git

### **Step 1: Clone Repository**
```bash
git clone https://github.com/youssef324/Doctor-Defense.git
cd Doctor-Defense
git checkout UI-v.1
```

### **Step 2: Create Virtual Environment**
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### **Step 5: Initialize Database**
```bash
flask db upgrade
```

### **Step 6: Generate Keys**
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### **Step 7: Run Application**
```bash
# Development
python run.py

# Production
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### **Access Application**
```
http://localhost:5000
```

---

## 📖 Usage Guide

### **Registration & Login**

1. **Create Account**
   - Visit `/auth/register`
   - Enter username, email, password
   - Password must have: 8+ chars, uppercase, number

2. **First Login**
   - Enter credentials
   - Will redirect to 2FA setup
   - Scan QR code with authenticator app (Google Authenticator, Authy, etc.)
   - Confirm 2FA code

3. **OAuth Login**
   - Click "Continue with Google" or "Continue with GitHub"
   - Authorize application
   - Account auto-created if new

### **Document Upload**

1. **Upload Interface**
   - Go to `/upload` from dashboard
   - Drag-and-drop files or click to select
   - Enter encryption password
   - Click "Upload"

2. **Encryption Process**
   - File encrypted with AES-256-GCM
   - Digital signature created
   - Stored in encrypted form

3. **Upload Verification**
   - See success message
   - Document appears in dashboard

### **Document Download & Verification**

1. **Download Document**
   - Click "Download" on dashboard
   - Enter encryption password
   - File automatically decrypted
   - Signature verified

2. **Verify Integrity**
   - Click "Verify" on document
   - Enter password
   - See verification status
   - ✅ Not tampered / ❌ Tampered

### **Admin Operations**

1. **Manage Users**
   - Go to `/admin/users`
   - View all users
   - Change user roles
   - Modify permissions

2. **View All Documents**
   - Go to `/admin/all-documents`
   - See documents across platform
   - Verify document integrity
   - Track document metadata

---

## 🔐 Security Features

### **Encryption Security**

```python
# AES-256-GCM with Scrypt Key Derivation
Encryption: salt (16 bytes) || nonce (12 bytes) || ciphertext
Key Derivation: scrypt(n=16384, r=8, p=1, dklen=32)
Authentication: AESGCM provides authenticated encryption (AEAD)
```

### **Authentication Security**

```python
# Password Storage
Algorithm: Bcrypt with 12 rounds
Never stored in plaintext
Passwords hashed on registration and verified on login

# Token Management
Type: JWT (JSON Web Tokens)
Storage: Secure HTTP-only cookies
Expiration: 2 hours
Refresh: Re-login required
```

### **2FA Security**

```python
# Time-based One-Time Password (TOTP)
Algorithm: RFC 6238
Provider: PyOTP
Authenticator Apps: Google Authenticator, Authy, Microsoft Authenticator
Backup: Secret key stored in database
```

### **Communication Security**

```
HTTPS Enforcement:
- Automatic HTTP → HTTPS redirect in production
- HSTS header: max-age=31536000; includeSubDomains
- Forces HTTPS for all subsequent requests
- Prevents MITM attacks
```

### **API Security**

```
JWT Verification:
- Every protected endpoint verifies JWT
- Tokens stored in HTTP-only cookies
- CSRF protection enabled
- Role-based access control enforced
```

---

## 🌐 Deployment

### **Docker Deployment**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

### **Docker Compose**

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/doctor_defense
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: doctor_defense
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

### **Nginx Configuration**

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### **Deployment Checklist**

- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure OAuth credentials (Google & GitHub)
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure reverse proxy (Nginx)
- [ ] Use production database (PostgreSQL)
- [ ] Set JWT_COOKIE_SECURE=True
- [ ] Configure backup strategy
- [ ] Setup monitoring and logging
- [ ] Test 2FA setup in production

---

## 🧪 Testing

### **Manual Testing Scenarios**

```bash
# Test 1: User Registration
- Visit /auth/register
- Create account with weak password (should fail)
- Create account with strong password (should succeed)

# Test 2: 2FA Setup
- Login with new account
- Scan QR code
- Enter incorrect code (should fail)
- Enter correct code (should succeed)

# Test 3: Document Upload & Encryption
- Upload file with password
- Verify file encrypted in storage
- Check file size matches

# Test 4: Document Verification
- Download document
- Verify signature validation
- Attempt download with wrong password (should fail)

# Test 5: RBAC Testing
- Create user with each role
- Test permission boundaries
- Verify unauthorized access blocked

# Test 6: OAuth Integration
- Test Google OAuth login
- Test GitHub OAuth login
- Verify auto-account creation
```

### **Security Testing**

```bash
# HTTPS Enforcement
curl -I http://localhost:5000  # Should redirect to HTTPS

# JWT Verification
# Attempt to access /dashboard without JWT - should fail
curl http://localhost:5000/dashboard

# CSRF Protection
# POST without CSRF token - should fail

# Password Policy
# Try to register with weak password - should fail
```

---

## 📚 Project Structure

```
Doctor-Defense/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── config.py                # Configuration settings
│   ├── models.py                # Database models (User, Document)
│   ├── run.py                   # Development server entry
│   │
│   ├── routes/
│   │   ├── auth.py              # Authentication routes (/auth/*)
│   │   ├── documents.py         # Document routes (/upload, /download)
│   │   ├── admin.py             # Admin routes (/admin/*)
│   │   └── oauth.py             # OAuth routes (/oauth/*)
│   │
│   ├── utils/
│   │   ├── crypto.py            # Encryption & signature functions
│   │   ├── decorators.py        # JWT & role decorators
│   │   └── validators.py        # Input validation
│   │
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── login.html           # Login page
│   │   ├── register.html        # Registration page
│   │   ├── 2fa_setup.html       # 2FA setup page
│   │   ├── dashboard.html       # User dashboard
│   │   ├── upload.html          # Upload page
│   │   ├── verify.html          # Document verification
│   │   └── admin_*.html         # Admin panel pages
│   │
│   └── static/
│       └── css/
│           └── style.css        # Custom styling
│
├── migrations/                  # Database migrations
│   └── versions/
│
├── instance/                    # Instance folder (local data)
│   ├── vault.db                 # SQLite database
│   └── private_key.pem          # RSA private key
│
├── uploads/                     # Encrypted documents storage
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── SECURITY_ENHANCEMENTS.md     # Security documentation
├── README.md                    # This file
└── LICENSE                      # MIT License

```

---

## 🤝 Contributing

### **Contributing Guidelines**

1. **Fork Repository**
   ```bash
   git clone https://github.com/youssef324/Doctor-Defense.git
   cd Doctor-Defense
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow PEP 8 style guide
   - Add docstrings
   - Test thoroughly

4. **Commit Changes**
   ```bash
   git commit -m "feat: Add your feature description"
   ```

5. **Push to Repository**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Describe changes
   - Reference related issues
   - Wait for review

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Youssef Ayman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 Support & Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/youssef324/Doctor-Defense/issues)
- **Email:** youssefjoeayman3@gmail.com
- **Documentation:** See [SECURITY_ENHANCEMENTS.md](SECURITY_ENHANCEMENTS.md)

---

## 🎓 Educational Resources

### **Security Concepts**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Cryptography Best Practices](https://cryptography.io/)
- [Flask Security](https://flask.palletsprojects.com/en/2.2.x/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

### **Development Resources**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Python Cryptography Library](https://cryptography.io/)

---

<div align="center">
  <h3>⭐ If you found this project helpful, please consider giving it a star!</h3>
  
  **Made with ❤️ by Youssef Ayman**
  
  [⬆ Back to Top](#-doctor-defense-secure-document-vault-system)
</div>
