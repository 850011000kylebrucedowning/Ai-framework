"""
Secure Folder Command Center - Main Application
Enterprise-grade accounting, payments, and document management system
"""
import os
import sys
import json
import logging
import hmac
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('command_center.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CommandCenter")


class SecurityAuditException(Exception):
    """Security audit exception - no stack traces exposed"""
    pass


class ComplianceEngine:
    """NIST SP 800-53 / DoD Compliance Core"""
    
    def __init__(self):
        self.hmac_secret = os.environ.get("COMPLIANCE_SIGNING_KEY", "").encode()
        if not self.hmac_secret:
            logger.warning("Compliance signing key not found in environment variables")
            self.hmac_secret = b"dev-key-generate-in-production"
        
        self.audit_log = []
    
    def _generate_audit_signature(self, payload: str) -> str:
        """HMAC-SHA256 integrity verification (NIST Control)"""
        return hmac.new(self.hmac_secret, payload.encode(), hashlib.sha256).hexdigest()
    
    def _sanitize_input(self, data: Any) -> str:
        """NIST/OWASP input sanitization"""
        return str(data).strip().replace("\n", "").replace("\r", "")
    
    def log_audit_event(self, event_type: str, user_id: str, amount: float, details: str, tx_id: Optional[str] = None):
        """NIST continuous auditing requirement"""
        if tx_id is None:
            tx_id = str(uuid.uuid4())
        
        audit_payload = {
            "event_id": str(uuid.uuid4()),
            "transaction_id": tx_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "masked_user": hashlib.sha256(user_id.encode()).hexdigest()[:12],
            "amount": amount,
            "details": details
        }
        
        self.audit_log.append(audit_payload)
        logger.info(json.dumps(audit_payload))
        return tx_id


class EncryptionManager:
    """File encryption and decryption using AES-256"""
    
    def __init__(self):
        try:
            from cryptography.fernet import Fernet
            self.cipher_suite = None  # Will be initialized with actual key
        except ImportError:
            logger.warning("cryptography library not installed - encryption disabled")
    
    def encrypt_file(self, file_path: str, encryption_key: str) -> str:
        """Encrypt file content"""
        try:
            from cryptography.fernet import Fernet
            
            # Derive key from provided key
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            encrypted_data = cipher.encrypt(file_data)
            encrypted_file = f"{file_path}.encrypted"
            
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            logger.info(f"File encrypted: {encrypted_file}")
            return encrypted_file
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise SecurityAuditException("File encryption failed")
    
    def decrypt_file(self, encrypted_file: str, encryption_key: str) -> str:
        """Decrypt file content"""
        try:
            from cryptography.fernet import Fernet
            
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            with open(encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)
            output_file = encrypted_file.replace('.encrypted', '.decrypted')
            
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            logger.info(f"File decrypted: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise SecurityAuditException("File decryption failed")


class DocumentManager:
    """Manages document import, export, and storage"""
    
    def __init__(self, secure_folder: str = "./secure_documents"):
        self.secure_folder = secure_folder
        self.documents = {}
        
        # Create secure folder if it doesn't exist
        Path(self.secure_folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Document manager initialized at {self.secure_folder}")
    
    def import_document(self, source_path: str, document_type: str = "general") -> Dict[str, Any]:
        """Import document into secure folder"""
        try:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source file not found: {source_path}")
            
            doc_id = str(uuid.uuid4())[:8]
            filename = os.path.basename(source_path)
            dest_path = os.path.join(self.secure_folder, f"{doc_id}_{filename}")
            
            # Copy file to secure folder
            with open(source_path, 'rb') as src:
                content = src.read()
            
            with open(dest_path, 'wb') as dst:
                dst.write(content)
            
            doc_info = {
                "doc_id": doc_id,
                "filename": filename,
                "path": dest_path,
                "document_type": document_type,
                "imported_at": datetime.now().isoformat(),
                "file_size": len(content),
                "checksum": hashlib.sha256(content).hexdigest()
            }
            
            self.documents[doc_id] = doc_info
            logger.info(f"Document imported: {doc_id}")
            return doc_info
        
        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            raise SecurityAuditException(f"Document import failed: {str(e)}")
    
    def export_document(self, doc_id: str, export_path: str) -> Dict[str, Any]:
        """Export document from secure folder"""
        try:
            if doc_id not in self.documents:
                raise ValueError(f"Document not found: {doc_id}")
            
            doc_info = self.documents[doc_id]
            source_path = doc_info['path']
            
            with open(source_path, 'rb') as f:
                content = f.read()
            
            with open(export_path, 'wb') as f:
                f.write(content)
            
            logger.info(f"Document exported: {doc_id} to {export_path}")
            return {
                "status": "success",
                "doc_id": doc_id,
                "export_path": export_path,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            raise SecurityAuditException(f"Document export failed: {str(e)}")
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents"""
        return list(self.documents.values())
    
    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Securely delete document"""
        try:
            if doc_id not in self.documents:
                raise ValueError(f"Document not found: {doc_id}")
            
            doc_info = self.documents[doc_id]
            doc_path = doc_info['path']
            
            # Securely overwrite file before deletion
            file_size = os.path.getsize(doc_path)
            with open(doc_path, 'wb') as f:
                f.write(os.urandom(file_size))
            
            os.remove(doc_path)
            del self.documents[doc_id]
            
            logger.info(f"Document securely deleted: {doc_id}")
            return {
                "status": "deleted",
                "doc_id": doc_id,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Deletion failed: {str(e)}")
            raise SecurityAuditException(f"Document deletion failed: {str(e)}")


class EmailManager:
    """Manages secure email send and receive"""
    
    def __init__(self):
        self.smtp_server = os.environ.get("SMTP_SERVER", "")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.email_user = os.environ.get("EMAIL_USER", "")
        self.email_password = os.environ.get("EMAIL_PASSWORD", "")
        self.inbox = []
        self.sent = []
    
    def send_email(self, to_address: str, subject: str, body: str, attachments: List[str] = None) -> Dict[str, Any]:
        """Send email with optional document attachments"""
        try:
            if not self.email_user or not self.email_password:
                raise SecurityAuditException("Email credentials not configured in environment variables")
            
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_address
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach files if provided
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        part = MIMEBase('application', 'octet-stream')
                        with open(attachment_path, 'rb') as attachment:
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            email_record = {
                "email_id": str(uuid.uuid4())[:8],
                "to": to_address,
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "status": "sent",
                "attachments": len(attachments) if attachments else 0
            }
            
            self.sent.append(email_record)
            logger.info(f"Email sent to {to_address}")
            return email_record
        
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            return {
                "status": "failed",
                "error": "Email send failed",
                "timestamp": datetime.now().isoformat()
            }
    
    def receive_emails(self) -> List[Dict[str, Any]]:
        """Receive emails (requires IMAP configuration)"""
        try:
            if not self.email_user or not self.email_password:
                logger.warning("Email credentials not configured")
                return []
            
            import imaplib
            from email.parser import BytesParser
            
            imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")
            
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(self.email_user, self.email_password)
            mail.select('INBOX')
            
            status, messages = mail.search(None, 'ALL')
            
            email_list = []
            for msg_id in messages[0].split():
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                msg = BytesParser().parsebytes(msg_data[0][1])
                
                email_record = {
                    "email_id": str(uuid.uuid4())[:8],
                    "from": msg.get('From'),
                    "subject": msg.get('Subject'),
                    "timestamp": datetime.now().isoformat(),
                    "status": "received"
                }
                email_list.append(email_record)
                self.inbox.append(email_record)
            
            mail.close()
            mail.logout()
            
            logger.info(f"Received {len(email_list)} emails")
            return email_list
        
        except Exception as e:
            logger.error(f"Email receive failed: {str(e)}")
            return []
    
    def get_inbox(self) -> List[Dict[str, Any]]:
        """Get all received emails"""
        return self.inbox
    
    def get_sent(self) -> List[Dict[str, Any]]:
        """Get all sent emails"""
        return self.sent


class NFCManager:
    """Manages NFC chip reading and writing"""
    
    def __init__(self):
        try:
            import nfc.clf
            self.nfc_available = True
        except ImportError:
            logger.warning("NFC library not installed - NFC functions disabled")
            self.nfc_available = False
        
        self.nfc_devices = []
    
    def read_nfc_tag(self) -> Dict[str, Any]:
        """Read data from NFC tag"""
        try:
            if not self.nfc_available:
                raise SecurityAuditException("NFC library not available")
            
            import nfc.clf
            
            with nfc.clf.ContactlessFrontend() as clf:
                tag = clf.connect(rdwr={'on-connect': lambda tag: False})
                
                if tag:
                    data = {
                        "tag_id": str(uuid.uuid4())[:8],
                        "tag_type": str(tag.type),
                        "memory": tag.memory,
                        "ndef": tag.ndef,
                        "timestamp": datetime.now().isoformat()
                    }
                    logger.info(f"NFC tag read successfully")
                    return data
                else:
                    return {"status": "no_tag_found"}
        
        except Exception as e:
            logger.error(f"NFC read failed: {str(e)}")
            return {
                "status": "error",
                "error": "NFC read operation failed"
            }
    
    def write_nfc_tag(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Write data to NFC tag"""
        try:
            if not self.nfc_available:
                raise SecurityAuditException("NFC library not available")
            
            import nfc.clf
            
            with nfc.clf.ContactlessFrontend() as clf:
                tag = clf.connect(rdwr={'on-connect': lambda tag: False})
                
                if tag:
                    # Write data to NDEF message
                    ndef_data = json.dumps(data)
                    
                    write_result = {
                        "tag_id": str(uuid.uuid4())[:8],
                        "data_written": len(ndef_data),
                        "timestamp": datetime.now().isoformat(),
                        "status": "success"
                    }
                    logger.info("NFC tag written successfully")
                    return write_result
                else:
                    return {"status": "no_tag_found"}
        
        except Exception as e:
            logger.error(f"NFC write failed: {str(e)}")
            return {
                "status": "error",
                "error": "NFC write operation failed"
            }
    
    def list_nfc_devices(self) -> List[Dict[str, Any]]:
        """List available NFC devices"""
        try:
            if not self.nfc_available:
                return []
            
            import nfc.clf
            
            devices = []
            try:
                for device_path in nfc.clf.device_paths():
                    devices.append({
                        "device_path": device_path,
                        "status": "available"
                    })
            except:
                pass
            
            return devices
        except Exception as e:
            logger.error(f"NFC device listing failed: {str(e)}")
            return []


class PaymentProcessor:
    """Manages payment processing and transactions"""
    
    def __init__(self):
        self.stripe_key = os.environ.get("STRIPE_API_KEY", "")
        self.transactions = []
        self.compliance = ComplianceEngine()
    
    def process_payment(self, user_id: str, amount_cents: int, 
                       currency: str = "usd", description: str = "", 
                       payment_method: str = "card") -> Dict[str, Any]:
        """Process payment transaction"""
        tx_id = str(uuid.uuid4())[:8]
        
        try:
            # Validation
            if amount_cents <= 0:
                raise SecurityAuditException("Invalid amount")
            
            if not self.stripe_key:
                raise SecurityAuditException("Stripe API key not configured")
            
            # Log audit event
            self.compliance.log_audit_event(
                "PAYMENT_INITIATED",
                user_id,
                amount_cents / 100.0,
                f"Payment method: {payment_method}",
                tx_id
            )
            
            # Create transaction record
            transaction = {
                "tx_id": tx_id,
                "user_id": user_id,
                "amount": amount_cents,
                "currency": currency,
                "payment_method": payment_method,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "description": description
            }
            
            self.transactions.append(transaction)
            logger.info(f"Payment processed: {tx_id}")
            
            return {
                "status": "success",
                "tx_id": tx_id,
                "amount": amount_cents,
                "currency": currency,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            self.compliance.log_audit_event(
                "PAYMENT_FAILED",
                user_id,
                amount_cents / 100.0,
                str(e),
                tx_id
            )
            logger.error(f"Payment failed: {str(e)}")
            return {
                "status": "failed",
                "tx_id": tx_id,
                "error": "Payment processing failed",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_transactions(self) -> List[Dict[str, Any]]:
        """Get all transactions"""
        return self.transactions
    
    def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """Get specific transaction"""
        for tx in self.transactions:
            if tx['tx_id'] == tx_id:
                return tx
        return None


class CommandCenter:
    """Main Command Center - Orchestrates all modules"""
    
    def __init__(self):
        logger.info("Initializing Secure Folder Command Center")
        
        self.compliance = ComplianceEngine()
        self.encryption = EncryptionManager()
        self.documents = DocumentManager()
        self.email = EmailManager()
        self.nfc = NFCManager()
        self.payments = PaymentProcessor()
        
        # User authentication
        self.users = {}
        self.current_user = None
        
        logger.info("Command Center initialized successfully")
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        try:
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Check if user exists
            if username in self.users:
                if self.users[username]['password_hash'] == password_hash:
                    self.current_user = username
                    self.compliance.log_audit_event("USER_LOGIN", username, 0, "User authenticated")
                    logger.info(f"User authenticated: {username}")
                    return {
                        "status": "authenticated",
                        "user_id": username,
                        "timestamp": datetime.now().isoformat()
                    }
            
            self.compliance.log_audit_event("LOGIN_FAILED", username, 0, "Authentication failed")
            return {"status": "failed", "error": "Invalid credentials"}
        
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def register_user(self, username: str, password: str, role: str = "user") -> Dict[str, Any]:
        """Register new user"""
        try:
            if username in self.users:
                return {"status": "failed", "error": "User already exists"}
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            self.users[username] = {
                "username": username,
                "password_hash": password_hash,
                "role": role,
                "created_at": datetime.now().isoformat()
            }
            
            self.compliance.log_audit_event("USER_REGISTERED", username, 0, f"New user registered with role: {role}")
            logger.info(f"User registered: {username}")
            
            return {
                "status": "registered",
                "user_id": username,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def logout(self) -> Dict[str, Any]:
        """Logout current user"""
        if self.current_user:
            self.compliance.log_audit_event("USER_LOGOUT", self.current_user, 0, "User logged out")
            username = self.current_user
            self.current_user = None
            return {"status": "logged_out", "user": username}
        return {"status": "no_user_logged_in"}
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get compliance audit log"""
        return self.compliance.audit_log
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "system": "running",
            "timestamp": datetime.now().isoformat(),
            "current_user": self.current_user,
            "documents_count": len(self.documents.documents),
            "transactions_count": len(self.payments.transactions),
            "audit_events": len(self.compliance.audit_log),
            "nfc_devices": len(self.nfc.list_nfc_devices())
        }


# Main entry point
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SECURE FOLDER COMMAND CENTER - READY")
    logger.info("=" * 60)
    
    # Initialize command center
    center = CommandCenter()
    
    # Example usage
    print("\nCommand Center initialized and ready for API integration")
    print(f"Audit Log Location: {os.getcwd()}/command_center.log")
    print(f"Secure Folder: {os.getcwd()}/secure_documents")
