import pymongo
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "secure_transactions_db"

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = client[DB_NAME]
    
    verified_collection = db["verified_data"]
    alert_collection = db["security_alerts"]
    
    client.server_info() 
    DB_AVAILABLE = True
    print("MongoDB Connection: SUCCESS")
    
except Exception as e:
    DB_AVAILABLE = False
    print("MongoDB Connection: OFFLINE (Is MongoDB installed and running?)")

def save_verified_data(payload: dict, raw_token: str, client_ip: str, user_agent: str):
    """Saves authentic data and network intelligence into the database."""
    if not DB_AVAILABLE: 
        return None
        
    document = {
        "status": "SUCCESS",
        "transaction_details": {
            "transaction_id": payload.get("transaction_id"),
            "sender": payload.get("sender"),
            "receiver": payload.get("receiver"),
            "amount": payload.get("amount")
        },
        "network_intelligence": {
            "client_ip": client_ip,
            "device_used": user_agent,
            "timestamp": datetime.utcnow()
        },
        "raw_jwt": raw_token
    }
    result = verified_collection.insert_one(document)
    return result.inserted_id

def log_security_alert(reason: str, raw_token: str, tampered_payload: dict, client_ip: str, user_agent: str):
    """Logs a Man-in-the-Middle attack attempt with full threat intelligence."""
    if not DB_AVAILABLE: 
        return None
        
    document = {
        "status": "FAILED_ATTACK",
        "reason": reason,
        "attempted_transaction": {
            "transaction_id": tampered_payload.get("transaction_id"),
            "sender": tampered_payload.get("sender"),
            "receiver": tampered_payload.get("receiver"),
            "fraudulent_amount": tampered_payload.get("amount")
        },
        "threat_intelligence": {
            "attacker_ip": client_ip,
            "device_used": user_agent,
            "attack_time": datetime.utcnow()
        },
        "raw_jwt": raw_token
    }
    result = alert_collection.insert_one(document)
    return result.inserted_id