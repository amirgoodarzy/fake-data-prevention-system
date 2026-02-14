import os
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEYS_DIR = "keys"
os.makedirs(KEYS_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")

def generate_keys():
    
    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    public_key = private_key.public_key()
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_private_key():
    
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return f.read()

def load_public_key():
    
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return f.read()

def sign_data(payload: dict) -> str:
    
    private_key = load_private_key()
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

def verify_data(token: str):
    
    public_key = load_public_key()
    try:
        decoded_payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return True, decoded_payload
        
    except jwt.ExpiredSignatureError:
        return False, "Token has expired."
    except jwt.InvalidTokenError:
        return False, "Fake data detected: Invalid signature."

if __name__ == "__main__":
    generate_keys()