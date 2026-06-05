# Secure Folder Structure

This folder contains the complete **Secure Folder Command Center** application.

## 📁 Folder Structure

```
secure_center/
├── command_center.py          # Core Command Center engine
├── api_server.py              # Flask REST API server
├── gui.py                     # PyQt5 desktop application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment configuration template
├── secure_documents/         # Encrypted document storage (auto-created)
├── logs/                     # Application logs (auto-created)
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd secure_center
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

### 3. Run Application

**Desktop GUI:**
```bash
python gui.py
```

**REST API Server:**
```bash
python api_server.py
```

**Command Line:**
```bash
python command_center.py
```

## 🔐 Security Features

- NIST SP 800-53 compliant audit logging
- AES-256 file encryption
- HMAC-SHA256 cryptographic signatures
- Secure file deletion (overwrite before removal)
- Role-based access control (RBAC)
- PII obfuscation in audit logs
- Immutable transaction history

## 📦 Components

### command_center.py
Core application with:
- ComplianceEngine - NIST auditing
- EncryptionManager - File encryption/decryption
- DocumentManager - Secure document storage
- EmailManager - Email integration
- NFCManager - NFC tag read/write
- PaymentProcessor - Payment processing
- CommandCenter - Main orchestrator

### api_server.py
Flask REST API with endpoints for:
- Authentication (register, login, logout)
- Documents (import, export, list, delete)
- Email (send, receive, inbox, sent)
- NFC (read, write, list devices)
- Payments (process, get transactions)
- System (status, audit log)

### gui.py
PyQt5 desktop application with:
- Authentication tab
- Document management
- Email integration
- NFC device control
- Payment processing
- Audit log viewer
- System status dashboard

## 🔗 Integration Points

Ready to integrate with:
- **Banking**: Stripe, Synapse, Treasury Prime
- **Email**: Gmail, Office 365, Custom SMTP/IMAP
- **NFC**: Feig, Baltech, PN532, ISO14443A readers
- **Cloud**: AWS KMS, Azure Key Vault, Google Cloud

## 📝 Environment Variables

Create `.env` file:
```env
COMPLIANCE_SIGNING_KEY=your_min_32_char_secret_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
STRIPE_API_KEY=sk_test_your_key
ENCRYPTION_KEY=your_encryption_key
```

## 📊 Usage Examples

### Import and Share Document
```python
from command_center import CommandCenter

center = CommandCenter()
center.register_user("john", "password123", "admin")
center.authenticate_user("john", "password123")

# Import contract
doc = center.documents.import_document("contract.pdf", "contract")

# Send via email
center.email.send_email(
    "recipient@example.com",
    "Contract Review",
    "Please review attached",
    [doc['path']]
)
```

### Process Payment
```python
# Process transaction
payment = center.payments.process_payment(
    "john",
    250000,  # $2,500.00
    "usd",
    "Invoice #123"
)

# View audit trail
audit_log = center.get_audit_log()
```

### Write to NFC
```python
# Credential data
cred = {
    "type": "certification",
    "user": "john_doe",
    "level": "SECRET"
}

# Write to chip
center.nfc.write_nfc_tag(cred)
```

## 🎯 Features at a Glance

| Feature | Status | Details |
|---------|--------|---------|
| Document Import/Export | ✅ | Secure folder storage |
| Email Integration | ✅ | SMTP/IMAP ready |
| NFC Read/Write | ✅ | Chip provisioning |
| Payment Processing | ✅ | Stripe-ready |
| Audit Logging | ✅ | NIST SP 800-53 |
| Encryption | ✅ | AES-256 ready |
| RBAC | ✅ | Admin/Accountant/User |
| REST API | ✅ | Flask endpoints |
| Desktop GUI | ✅ | PyQt5 interface |

## ⚠️ Security Notes

### Never
- ❌ Commit `.env` to version control
- ❌ Hardcode API keys
- ❌ Share COMPLIANCE_SIGNING_KEY
- ❌ Log sensitive data
- ❌ Use development keys in production

### Always
- ✅ Use environment variables
- ✅ Rotate keys regularly
- ✅ Review audit logs
- ✅ Use HTTPS in production
- ✅ Implement backups
- ✅ Test encryption

## 📞 Support

For issues or questions:
1. Check logs: `command_center.log`
2. Verify `.env` configuration
3. Ensure all dependencies installed
4. Review API responses

## 🔄 Next Steps

1. Configure `.env` with credentials
2. Test locally (GUI or API)
3. Connect real banking APIs
4. Set up production deployment
5. Implement backup strategy
6. Schedule security audits

---

**Built with enterprise-grade security and compliance**
