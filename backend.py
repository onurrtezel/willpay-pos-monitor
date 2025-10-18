"""
WillPay Backend API
Handles receipt creation, token generation, and receipt retrieval
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
import hmac
import hashlib
import datetime
import json

app = Flask(__name__)
CORS(app)

SECRET_KEY = "willpay_secret_key_2025"
DB_NAME = "willpay.db"


def init_db():
    """Initialize SQLite database with receipts and receipt_items tables"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Receipts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            store_name TEXT,
            total_amount REAL,
            category TEXT,
            date TEXT,
            notes TEXT,
            token TEXT UNIQUE,
            created_at TEXT
        )
    """)
    
    # Receipt items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipt_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER,
            name TEXT,
            price REAL,
            quantity INTEGER,
            category TEXT,
            created_at TEXT,
            FOREIGN KEY (receipt_id) REFERENCES receipts (id)
        )
    """)
    
    conn.commit()
    conn.close()


def generate_token():
    """Generate secure token using UUID + HMAC_SHA256"""
    token_uuid = str(uuid.uuid4())
    timestamp = str(datetime.datetime.now().timestamp())
    
    # Create HMAC signature
    message = f"{token_uuid}{timestamp}".encode()
    signature = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
    
    # Combine UUID and signature
    token = f"{token_uuid}-{signature[:16]}"
    return token


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "WillPay API"}), 200


@app.route('/receipts', methods=['POST'])
def create_receipt():
    """
    Create new receipt with items
    Expected JSON:
    {
        "store_name": "Granny's Waffle",
        "items": [
            {"name": "Çikolatalı Waffle", "price": 35, "quantity": 1, "category": "Waffle"}
        ],
        "totalAmount": 90,
        "user_id": "optional",
        "notes": "optional"
    }
    """
    try:
        data = request.json
        
        if not data or 'items' not in data or 'totalAmount' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Generate token
        token = generate_token()
        created_at = datetime.datetime.now().isoformat()
        
        # Insert receipt
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO receipts 
            (user_id, store_name, total_amount, category, date, notes, token, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('user_id', 'anonymous'),
            data.get('store_name', 'Granny\'s Waffle'),
            data['totalAmount'],
            data.get('category', 'General'),
            created_at,
            data.get('notes', ''),
            token,
            created_at
        ))
        
        receipt_id = cursor.lastrowid
        
        # Insert receipt items
        for item in data['items']:
            cursor.execute("""
                INSERT INTO receipt_items 
                (receipt_id, name, price, quantity, category, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                item['name'],
                item['price'],
                item['quantity'],
                item.get('category', 'General'),
                created_at
            ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "receipt_id": receipt_id,
            "token": token,
            "qr_url": f"https://willpay.app/receipt?token={token}",
            "created_at": created_at
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt(receipt_id):
    """Get receipt details by ID"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get receipt
        cursor.execute("SELECT * FROM receipts WHERE id = ?", (receipt_id,))
        receipt = cursor.fetchone()
        
        if not receipt:
            return jsonify({"error": "Receipt not found"}), 404
        
        # Get receipt items
        cursor.execute("SELECT * FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        items = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "receipt": dict(receipt),
            "items": [dict(item) for item in items]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/receipts/token/<token>', methods=['GET'])
def get_receipt_by_token(token):
    """Get receipt details by token (for QR scanning)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get receipt by token
        cursor.execute("SELECT * FROM receipts WHERE token = ?", (token,))
        receipt = cursor.fetchone()
        
        if not receipt:
            return jsonify({"error": "Invalid or expired token"}), 404
        
        receipt_id = receipt['id']
        
        # Get receipt items
        cursor.execute("SELECT * FROM receipt_items WHERE receipt_id = ?", (receipt_id,))
        items = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            "success": True,
            "receipt": dict(receipt),
            "items": [dict(item) for item in items]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/notify/receipt/<int:receipt_id>', methods=['POST'])
def notify_receipt(receipt_id):
    """
    Notify mobile app about receipt scan
    This would trigger push notification to user's mobile device
    """
    try:
        data = request.json or {}
        
        # In production, this would send push notification
        # For PoC, just return success
        
        return jsonify({
            "success": True,
            "receipt_id": receipt_id,
            "notification_sent": True,
            "message": "Receipt notification sent to mobile app"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Initializing WillPay Backend...")
    init_db()
    print("✅ Database initialized")
    print("🌐 Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

