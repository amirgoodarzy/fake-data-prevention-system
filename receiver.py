import os
import json
from core.crypto_utils import verify_data
from core.db_handler import save_verified_data, log_security_alert

def receive_and_verify_data():
    print("--- RECEIVER PROCESS INITIATED ---")
    
    token_path = "transmitted_token.txt"
    if not os.path.exists(token_path):
        print("Error: No token found. Execute sender script first.")
        return

    with open(token_path, "r") as f:
        received_token = f.read().strip()
        
    print("Token Retrieved from Network.")
    print("Verifying Signature with Public Key...")
    
    is_valid, result = verify_data(received_token)

    if is_valid:
        print("\nSUCCESS: Data is Authentic.")
        print("Decoded Payload:")
        print(json.dumps(result, indent=2, default=str))
        
        print("\nSaving verified transaction to database...")
        db_id = save_verified_data(result, received_token)
        if db_id:
            print(f"Successfully saved to MongoDB (ID: {db_id})")
        
    else:
        print("\nSECURITY ALERT")
        print(f"Reason: {result}")
        print("Action: Transaction Blocked. Logging security incident...")
        
        db_id = log_security_alert(result, received_token)
        if db_id:
            print(f"Alert successfully logged to MongoDB (ID: {db_id})")
        

if __name__ == "__main__":
    receive_and_verify_data()