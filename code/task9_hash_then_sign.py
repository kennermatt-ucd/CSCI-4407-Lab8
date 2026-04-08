"""
Task 9 – Hash-then-Sign
Hash the message with SHA-256 first, then sign the digest.
Demonstrates that hashing removes the multiplicative structure
exploited in Task 8 and makes the scheme secure for arbitrary messages.
"""

import hashlib
import os
from cryptography.hazmat.primitives import serialization
from task7_plain_rsa import plain_rsa_sign, plain_rsa_verify

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH  = os.path.join(BASE_DIR, "messages", "message1.txt")
PRIV_PATH = os.path.join(BASE_DIR, "private_key.pem")


def load_rsa_components(priv_path: str):
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    priv_nums = private_key.private_numbers()
    pub_nums  = private_key.public_key().public_numbers()
    return pub_nums.n, pub_nums.e, priv_nums.d


def hash_message(message: bytes) -> int:
    """SHA-256 digest as an integer (suitable for raw RSA operations)."""
    digest = hashlib.sha256(message).digest()
    return int.from_bytes(digest, byteorder="big")


def main():
    n, e, d = load_rsa_components(PRIV_PATH)

    with open(MSG_PATH, "rb") as f:
        message = f.read()

    # Sign
    digest = hash_message(message)
    sig    = plain_rsa_sign(digest, d, n)

    # Verify — original message
    recovered_digest = plain_rsa_verify(sig, e, n)
    valid_original   = (recovered_digest == digest)

    # Verify — tampered message
    tampered        = message + b" [TAMPERED]"
    tampered_digest = hash_message(tampered)
    valid_tampered  = (plain_rsa_verify(sig, e, n) == tampered_digest)

    print("=== Task 9: Hash-then-Sign ===\n")
    print(f"Message          : {message.decode().strip()}")
    print(f"SHA-256 digest   : {hashlib.sha256(message).hexdigest()}")
    print(f"Signature (trunc): {str(sig)[:40]}...")
    print()
    print(f"Verify original message  : {'VALID' if valid_original else 'INVALID'}")
    print(f"Verify tampered message  : {'VALID' if valid_tampered else 'INVALID'}")
    print("\nConclusion: hashing destroys the multiplicative structure,")
    print("blocking the forgery attack from Task 8.")


if __name__ == "__main__":
    main()
