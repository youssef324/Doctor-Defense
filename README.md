# 🏥 Doctor-Defense: Secure Document Vault System

<p align="center">
  <b>
    A modern, enterprise-grade secure document management platform with end-to-end encryption,
    digital signatures, and role-based access control.
  </b>
</p>

---

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,postgresql,bootstrap,docker,nginx,github,git,vscode&theme=dark" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge&logo=jsonwebtokens" />
  <img src="https://img.shields.io/badge/OAuth-Google%20%26%20GitHub-blue?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/Encryption-AES256-success?style=for-the-badge&logo=letsencrypt" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge" />
</p>

<p align="center">
  <a href="#-features">🚀 Features</a> •
  <a href="#-architecture">🏗 Architecture</a> •
  <a href="#-installation--setup">⚙️ Installation</a> •
  <a href="#-security-features">🔐 Security</a> •
  <a href="#-deployment">🌐 Deployment</a>
</p>

---

# 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🏗 Architecture](#-architecture)
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

# 🎯 Overview

**Doctor-Defense** is a secure, enterprise-grade document management system designed to protect sensitive information using military-grade encryption, digital signatures, and comprehensive access control mechanisms.

## Core Highlights

- 🔐 AES-256-GCM Encryption
- 🖊️ RSA-2048 Digital Signatures
- 👥 Role-Based Access Control (RBAC)
- 🔑 Mandatory Two-Factor Authentication (2FA)
- 🌐 OAuth Authentication
- 📊 Responsive Modern Dashboard

---

# ✨ Features

## 🔐 Security Features

- AES-256-GCM Encryption
- RSA-2048 Digital Signatures
- TOTP-based Two-Factor Authentication
- Bcrypt Password Hashing
- OAuth 2.0 Authentication
- HTTPS Enforcement
- CSP Security Headers
- CSRF Protection
- JWT Authentication

---

## 📁 Document Management

- Multi-file Upload
- Drag & Drop Support
- Automatic Encryption on Upload
- Digital Signature Generation
- File Integrity Verification
- File Metadata Tracking
- Role-Based Sharing
- File Type Validation
- Maximum Upload Size: 50MB

---

## 👥 User Management

- User Registration System
- Role Assignment System
- Admin Dashboard
- JWT Session Management
- User Activity Logging

---

## 🎨 User Experience

- Responsive Bootstrap 5 Interface
- AJAX File Upload
- Real-Time Notifications
- Dark Theme Dashboard
- Interactive User Interface

---

# 🏗 Architecture

## System Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (UI Layer)                         │
│ ┌────────────────┬────────────────┬─────────────────────────┐  │
│ │ Dashboard      │ Upload Portal  │ Admin Panel             │  │
│ │ HTML/CSS/JS    │ HTML/CSS/JS    │ HTML/CSS/JS             │  │
│ └────────────────┴────────────────┴─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                     Backend API Layer                          │
│ ┌──────────────┬────────────────┬───────────────────────────┐ │
│ │ Auth Routes  │ Document APIs  │ Admin APIs                │ │
│ │ /auth/*      │ /upload        │ /admin/*                  │ │
│ │ /oauth/*     │ /download      │ /admin/users              │ │
│ └──────────────┴────────────────┴───────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```
---

# 👥 User Roles & Permissions

| Feature | Admin | Manager | User |
| --- | --- | --- | --- |
| Manage Users | ✅ | ❌ | ❌ |
| Modify Roles | ✅ | ❌ | ❌ |
| View All Documents | ✅ | ✅ | ❌ |
| Verify Documents | ✅ | ✅ | ❌ |
| Upload Documents | ✅ | ✅ | ✅ |
| Download Own Documents | ✅ | ✅ | ✅ |
| Delete Own Documents | ✅ | ✅ | ✅ |
| Access Admin Panel | ✅ | ❌ | ❌ |
| View Dashboard | ✅ | ✅ | ✅ |
```
```


# 🚀 Installation & Setup

## Clone Repository

```bash
git clone https://github.com/youssef324/Doctor-Defense.git

cd Doctor-Defense

git checkout UI-v.1
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python run.py
```

---

# 📚 Project Structure

```text
Doctor-Defense/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── run.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── documents.py
│   │   ├── admin.py
│   │   └── oauth.py
│   │
│   ├── utils/
│   │   ├── crypto.py
│   │   ├── decorators.py
│   │   └── validators.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── upload.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── migrations/
├── instance/
├── uploads/
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

---

# 📄 License

MIT License © 2026 Youssef Ayman

---

# ⭐ If you found this project useful, 
consider giving it a star!

Made with ❤️ by **Youssef Ayman**