import json
import datetime
from core.crypto_utils import sign_data

def create_and_send_data():
    print("--- SENDER PROCESS INITIATED ---")
    
    payload = {
        "transaction_id": "TXN-98765",
        "sender": "Alice",
        "receiver": "Bob",
        "amount": 5000,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10) 
    }
    
    print("Original Data Payload:")
    print(json.dumps(payload, indent=2, default=str))

    print("\nSigning data with Private Key...")
    secure_token = sign_data(payload)
    
    print("Data Successfully Signed. JWT Generated.")
    print(f"Token String:\n{secure_token}\n")

    with open("transmitted_token.txt", "w") as f:
        f.write(secure_token)
        
    print("Token saved to 'transmitted_token.txt' for transmission.")
    print("--------------------------------\n")

if __name__ == "__main__":
    create_and_send_data()