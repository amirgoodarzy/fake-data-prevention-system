from flask import Flask, render_template, jsonify, request
import json
import base64
import datetime
from core.crypto_utils import sign_data, verify_data
from core.db_handler import save_verified_data, log_security_alert

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/simulate_real', methods=['POST'])
def simulate_real():
    client_ip = request.remote_addr
    user_agent = request.user_agent.string

    payload = {
        "transaction_id": "TXN-11111",
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 5000,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    
    token = sign_data(payload)
    is_valid, result = verify_data(token)
    
    if is_valid:
        db_id = save_verified_data(result, token, client_ip, user_agent)
        return jsonify({"status": "success", "message": "Transaction Verified and Approved.", "db_id": str(db_id)})
    
    return jsonify({"status": "error", "message": result})

@app.route('/api/simulate_attack', methods=['POST'])
def simulate_attack():
    client_ip = request.remote_addr
    user_agent = request.user_agent.string

    payload = {
        "transaction_id": "TXN-22222",
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 5000,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    real_token = sign_data(payload)
    
    header, payload_b64, signature = real_token.split(".")
    padded = payload_b64 + "=" * (-len(payload_b64) % 4)
    payload_data = json.loads(base64.urlsafe_b64decode(padded).decode('utf-8'))
    
    payload_data["amount"] = 9999999 
    payload_data["receiver"] = "Eve"
    
    new_payload_b64 = base64.urlsafe_b64encode(json.dumps(payload_data).encode('utf-8')).decode('utf-8').rstrip('=')
    tampered_token = f"{header}.{new_payload_b64}.{signature}"
    
    is_valid, result = verify_data(tampered_token)
    
    if not is_valid:
        db_id = log_security_alert(result, tampered_token, payload_data, client_ip, user_agent)
        return jsonify({"status": "hacked", "message": "Fake Data Blocked: Invalid Signature.", "db_id": str(db_id)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)