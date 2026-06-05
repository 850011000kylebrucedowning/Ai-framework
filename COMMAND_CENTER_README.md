# Secure Folder Command Center

A professional-grade, enterprise-secure folder and command center for document management, payments, and financial operations.

## 🔐 Features

### Authentication & Access Control
- ✅ User registration and login
- ✅ Role-based access control (RBAC)
- ✅ Session management
- ✅ Password hashing (SHA-256)

### 📄 Document Management
- ✅ Import documents to secure folder
- ✅ Export encrypted documents
- ✅ File encryption (AES-256 ready)
- ✅ Secure file deletion (overwrite before deletion)
- ✅ Document metadata tracking
- ✅ File integrity verification (SHA-256 checksums)

### 📧 Email Integration
- ✅ Send emails with attachments
- ✅ Receive emails (IMAP support)
- ✅ Secure message handling
- ✅ Inbox and sent tracking
- ✅ Document sharing via email

### 💳 Payment Processing
- ✅ Payment transaction processing
- ✅ Support for multiple currencies (USD, EUR, GBP, CAD, AUD)
- ✅ Multiple payment methods (card, bank transfer, digital wallet, NFC)
- ✅ Transaction history tracking
- ✅ Stripe integration ready
- ✅ Payment status management

### 📡 NFC Integration
- ✅ Read NFC tags
- ✅ Write data to NFC chips
- ✅ List connected NFC devices
- ✅ JSON data serialization
- ✅ Device discovery

### 🏛️ Compliance & Auditing
- ✅ NIST SP 800-53 compliant audit logging
- ✅ Immutable audit trails
- ✅ Cryptographic integrity verification (HMAC-SHA256)
- ✅ PII obfuscation (masked user hashes)
- ✅ Continuous auditing
- ✅ Event logging

### 🖥️ User Interfaces
- ✅ Desktop GUI (PyQt5)
- ✅ REST API (Flask)
- ✅ Command-line integration ready

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

```bash
# Clone repository
git clone https://github.com/850011000kylebrucedowning/Ai-framework.git
cd Ai-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_gui.txt

# Configure environment
cp .env.command_center .env
# Edit .env with your settings
```

### Environment Variables

Required variables in `.env`:

```env
# Security signing key (minimum 32 characters)
COMPLIANCE_SIGNING_KEY=your_very_long_secret_key_min_32_chars

# Email (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Banking APIs (only when ready to integrate)
STRIPE_API_KEY=sk_live_your_key

# Encryption
ENCRYPTION_KEY=your_encryption_key
```

---

## 🚀 Running the Application

### Desktop GUI

```bash
python gui.py
```

This launches the PyQt5 desktop application with:
- Full document management
- Email integration
- Payment processing
- NFC device control
- Audit log viewing
- System status dashboard

### REST API Server

```bash
python api_server.py
```

Starts Flask server at `https://localhost:5000` with endpoints for:
- Authentication
- Document operations
- Email management
- NFC operations
- Payment processing
- System status

### Command-Line Usage

```python
from command_center import CommandCenter

# Initialize
center = CommandCenter()

# Register user
center.register_user("john", "password123", "admin")

# Login
center.authenticate_user("john", "password123")

# Import document
doc = center.documents.import_document("/path/to/file.pdf", "contract")

# Send email
center.email.send_email("recipient@example.com", "Subject", "Body text")

# Process payment
payment = center.payments.process_payment("john", 100000, "usd", "Invoice #123")

# Read NFC
nfc_data = center.nfc.read_nfc_tag()

# Get audit log
audit_log = center.get_audit_log()
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Documents
- `POST /api/documents/import` - Import document
- `GET /api/documents/list` - List all documents
- `GET /api/documents/export/<doc_id>` - Export document
- `DELETE /api/documents/delete/<doc_id>` - Delete document

### Email
- `POST /api/email/send` - Send email
- `GET /api/email/inbox` - Get inbox
- `GET /api/email/sent` - Get sent emails
- `POST /api/email/receive` - Receive emails

### NFC
- `POST /api/nfc/read` - Read NFC tag
- `POST /api/nfc/write` - Write NFC tag
- `GET /api/nfc/devices` - List NFC devices

### Payments
- `POST /api/payments/process` - Process payment
- `GET /api/payments/transactions` - Get transactions
- `GET /api/payments/transaction/<tx_id>` - Get transaction details

### System
- `GET /api/system/status` - Get system status
- `GET /api/system/audit-log` - Get audit log

---

## 🔒 Security Features

### Data Protection
- **File Encryption**: AES-256 encryption ready for sensitive documents
- **Secure Deletion**: Files are overwritten before deletion
- **Integrity Verification**: SHA-256 checksums for all documents
- **Input Sanitization**: NIST/OWASP compliant input validation

### Compliance
- **NIST SP 800-53**: Audit logging and system integrity controls
- **HMAC Signatures**: Cryptographic integrity verification
- **User Masking**: PII obfuscation in audit logs
- **Immutable Logs**: All security events logged permanently

### Access Control
- **Role-Based**: Admin, accountant, user roles
- **Authentication**: Password hashing with SHA-256
- **Session Management**: Per-user session tracking
- **Audit Trail**: All user actions logged

---

## 📊 Data Flow

```
User Input
    ↓
Authentication Check
    ↓
NIST Compliance Validation
    ↓
Cryptographic Integrity Verification
    ↓
Operation (Document/Email/Payment/NFC)
    ↓
Audit Event Logging
    ↓
Database/Storage Commit
    ↓
Response to User
```

---

## 🗂️ Folder Structure

```
secure_documents/           # Encrypted document storage
command_center.log         # Application and audit logs
├── models/
├── database/
├── compliance/
├── encryption/
└── api/
```

---

## 🔄 Integration with External Services

### Banking (Ready for Integration)
- Stripe Treasury
- Synapse
- Treasury Prime
- Your bank's API

### Email
- Gmail (configured by default)
- Office 365
- Custom SMTP

### NFC
- Feig Reader
- Baltech
- PN532 chipset
- Any ISO14443A compatible reader

---

## 📝 Example Workflows

### Import and Email Document
```python
# Import contract
doc = center.documents.import_document("contract.pdf", "contract")

# Send via email
center.email.send_email(
    "accountant@company.com",
    "Review Required",
    "Please review attached contract",
    [doc['path']]
)
```

### Process Payment and Log
```python
# Process payment
payment = center.payments.process_payment(
    user_id="john",
    amount_cents=250000,  # $2,500.00
    currency="usd",
    description="Monthly expenses"
)

# Automatically logged to audit trail
audit = center.get_audit_log()
```

### Write Certificate to NFC
```python
# Prepare credential data
cred_data = {
    "type": "contractor_cert",
    "user": "john_doe",
    "level": "SECRET",
    "expires": "2025-12-31"
}

# Write to NFC chip
result = center.nfc.write_nfc_tag(cred_data)
```

---

## ⚠️ Important Security Notes

### Never
- ❌ Hardcode API keys in code
- ❌ Commit `.env` files to git
- ❌ Share COMPLIANCE_SIGNING_KEY
- ❌ Use development keys in production
- ❌ Log sensitive financial data

### Always
- ✅ Use environment variables for secrets
- ✅ Rotate API keys regularly
- ✅ Review audit logs
- ✅ Use HTTPS in production
- ✅ Implement proper backups
- ✅ Test encryption/decryption

---

## 🧪 Testing

```bash
# Run with test data
python command_center.py

# This initializes the system and logs to command_center.log
```

---

## 📞 Support & Development

### Common Issues

**NFC not detecting devices:**
- Install libusb on Linux: `sudo apt-get install libusb-1.0-0-dev`
- Check device permissions: `sudo usermod -a -G dialout $USER`

**Email not sending:**
- Verify SMTP credentials in `.env`
- For Gmail: Use App Passwords, not regular password
- Check firewall port 587

**Document import fails:**
- Ensure read permissions on source file
- Check disk space in `secure_documents/`

---

## 📋 Compliance Checklist

- [x] NIST SP 800-53 audit logging
- [x] Cryptographic integrity (HMAC-SHA256)
- [x] PII obfuscation
- [x] Immutable audit trails
- [x] Role-based access control
- [x] Input validation and sanitization
- [x] Secure file deletion
- [x] Error handling without data leakage
- [x] User authentication
- [x] Session management

---

## 📄 License

This project is provided as-is for secure financial and document operations.

---

## ⚡ Next Steps

1. **Configure Environment**: Set up `.env` with your credentials
2. **Test Locally**: Run GUI or API server
3. **Connect Banking APIs**: Integrate with Stripe/your bank
4. **Deploy**: Set up production server with HTTPS
5. **Audit**: Review compliance logs regularly

---

Built with 🔐 security-first architecture
