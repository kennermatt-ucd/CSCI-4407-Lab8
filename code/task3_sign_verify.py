"""
Task 3 – Signing and Verification
Sign message1.txt with the RSA private key (RSA-PSS + SHA-256).
Verify the signature with the public key and confirm success.
"""

import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

BASE_DIR    = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH    = os.path.join(BASE_DIR, "messages", "message1.txt")
SIG_PATH    = os.path.join(BASE_DIR, "message1.sig")
PRIV_PATH   = os.path.join(BASE_DIR, "private_key.pem")
PUB_PATH    = os.path.join(BASE_DIR, "public_key.pem")


def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def sign_message(private_key, message: bytes) -> bytes:
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def main():
    private_key = load_private_key(PRIV_PATH)
    public_key  = load_public_key(PUB_PATH)

    with open(MSG_PATH, "rb") as f:
        message = f.read()

    signature = sign_message(private_key, message)

    with open(SIG_PATH, "wb") as f:
        f.write(signature)

    is_valid = verify_signature(public_key, message, signature)

    print("=== Task 3: Signing and Verification ===\n")
    print(f"Message           : {message.decode().strip()}")
    print(f"Signature (hex)   : {signature.hex()[:64]}...")
    print(f"Signature saved   : {SIG_PATH}")
    print(f"Verification      : {'VALID' if is_valid else 'INVALID'}")


if __name__ == "__main__":
    main()
