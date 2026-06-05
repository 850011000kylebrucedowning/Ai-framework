"""
REST API for Secure Folder Command Center
Provides endpoints for all command center functions
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import logging
import os
from dotenv import load_dotenv

from command_center import CommandCenter, SecurityAuditException

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize command center
center = CommandCenter()

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not center.current_user:
            return jsonify({"status": "error", "message": "Not authenticated"}), 401
        return f(*args, **kwargs)
    return decorated


# ============ AUTHENTICATION ENDPOINTS ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        
        result = center.register_user(username, password, role)
        return jsonify(result), 200 if result['status'] == 'registered' else 400
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        result = center.authenticate_user(username, password)
        return jsonify(result), 200 if result['status'] == 'authenticated' else 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user"""
    result = center.logout()
    return jsonify(result), 200


# ============ DOCUMENT MANAGEMENT ENDPOINTS ============

@app.route('/api/documents/import', methods=['POST'])
@require_auth
def import_document():
    """Import document into secure folder"""
    try:
        file = request.files['file']
        doc_type = request.form.get('type', 'general')
        
        # Save file temporarily
        temp_path = f"/tmp/{file.filename}"
        file.save(temp_path)
        
        # Import to secure folder
        result = center.documents.import_document(temp_path, doc_type)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Import error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/documents/export/<doc_id>', methods=['GET'])
@require_auth
def export_document(doc_id):
    """Export document from secure folder"""
    try:
        export_path = f"/tmp/export_{doc_id}.tmp"
        result = center.documents.export_document(doc_id, export_path)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/documents/list', methods=['GET'])
@require_auth
def list_documents():
    """List all documents"""
    try:
        documents = center.documents.list_documents()
        return jsonify({
            "status": "success",
            "count": len(documents),
            "documents": documents
        }), 200
    except Exception as e:
        logger.error(f"List error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/documents/delete/<doc_id>', methods=['DELETE'])
@require_auth
def delete_document(doc_id):
    """Delete document"""
    try:
        result = center.documents.delete_document(doc_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ EMAIL ENDPOINTS ============

@app.route('/api/email/send', methods=['POST'])
@require_auth
def send_email():
    """Send email"""
    try:
        data = request.get_json()
        to_address = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        attachments = data.get('attachments', [])
        
        result = center.email.send_email(to_address, subject, body, attachments)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Send email error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/email/inbox', methods=['GET'])
@require_auth
def get_inbox():
    """Get inbox"""
    try:
        inbox = center.email.get_inbox()
        return jsonify({
            "status": "success",
            "count": len(inbox),
            "messages": inbox
        }), 200
    except Exception as e:
        logger.error(f"Inbox error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/email/sent', methods=['GET'])
@require_auth
def get_sent():
    """Get sent emails"""
    try:
        sent = center.email.get_sent()
        return jsonify({
            "status": "success",
            "count": len(sent),
            "messages": sent
        }), 200
    except Exception as e:
        logger.error(f"Sent error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/email/receive', methods=['POST'])
@require_auth
def receive_emails():
    """Receive emails from server"""
    try:
        emails = center.email.receive_emails()
        return jsonify({
            "status": "success",
            "count": len(emails),
            "messages": emails
        }), 200
    except Exception as e:
        logger.error(f"Receive error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ NFC ENDPOINTS ============

@app.route('/api/nfc/read', methods=['POST'])
@require_auth
def read_nfc():
    """Read NFC tag"""
    try:
        result = center.nfc.read_nfc_tag()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"NFC read error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/nfc/write', methods=['POST'])
@require_auth
def write_nfc():
    """Write to NFC tag"""
    try:
        data = request.get_json()
        result = center.nfc.write_nfc_tag(data)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"NFC write error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/nfc/devices', methods=['GET'])
@require_auth
def list_nfc_devices():
    """List NFC devices"""
    try:
        devices = center.nfc.list_nfc_devices()
        return jsonify({
            "status": "success",
            "count": len(devices),
            "devices": devices
        }), 200
    except Exception as e:
        logger.error(f"NFC devices error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ PAYMENT ENDPOINTS ============

@app.route('/api/payments/process', methods=['POST'])
@require_auth
def process_payment():
    """Process payment"""
    try:
        data = request.get_json()
        user_id = center.current_user
        amount_cents = int(data.get('amount_cents', 0))
        currency = data.get('currency', 'usd')
        description = data.get('description', '')
        payment_method = data.get('payment_method', 'card')
        
        result = center.payments.process_payment(
            user_id, amount_cents, currency, description, payment_method
        )
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/payments/transactions', methods=['GET'])
@require_auth
def get_transactions():
    """Get all transactions"""
    try:
        transactions = center.payments.get_transactions()
        return jsonify({
            "status": "success",
            "count": len(transactions),
            "transactions": transactions
        }), 200
    except Exception as e:
        logger.error(f"Transactions error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/payments/transaction/<tx_id>', methods=['GET'])
@require_auth
def get_transaction(tx_id):
    """Get specific transaction"""
    try:
        transaction = center.payments.get_transaction(tx_id)
        if transaction:
            return jsonify({
                "status": "success",
                "transaction": transaction
            }), 200
        else:
            return jsonify({"status": "not_found"}), 404
    except Exception as e:
        logger.error(f"Transaction error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ SYSTEM ENDPOINTS ============

@app.route('/api/system/status', methods=['GET'])
@require_auth
def system_status():
    """Get system status"""
    try:
        status = center.get_system_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Status error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/system/audit-log', methods=['GET'])
@require_auth
def get_audit_log():
    """Get audit log"""
    try:
        audit_log = center.get_audit_log()
        return jsonify({
            "status": "success",
            "count": len(audit_log),
            "events": audit_log
        }), 200
    except Exception as e:
        logger.error(f"Audit log error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting Secure Folder Command Center API")
    logger.info("Available at http://localhost:5000")
    
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')
