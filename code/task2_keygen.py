"""
Task 2 – RSA Key Generation
Generate a 2048-bit RSA private key and derive the public key.
Export both to PEM files for use in subsequent tasks.
"""

import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEY_DIR = os.path.join(os.path.dirname(__file__), "..")


def generate_rsa_keypair(key_size: int = 2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    return private_key, private_key.public_key()


def save_private_key(private_key, path: str):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(path, "wb") as f:
        f.write(pem)


def save_public_key(public_key, path: str):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(path, "wb") as f:
        f.write(pem)


def main():
    private_key, public_key = generate_rsa_keypair(key_size=2048)

    private_path = os.path.join(KEY_DIR, "private_key.pem")
    public_path  = os.path.join(KEY_DIR, "public_key.pem")

    save_private_key(private_key, private_path)
    save_public_key(public_key, public_path)

    pub_numbers = public_key.public_key().public_numbers() \
        if hasattr(public_key, "public_key") else public_key.public_numbers()

    print("=== Task 2: RSA Key Generation ===\n")
    print(f"Key size        : {private_key.key_size} bits")
    print(f"Public exponent : {pub_numbers.e}")
    print(f"Private key     : {private_path}")
    print(f"Public key      : {public_path}")
    print("\nPublic key (PEM):")
    with open(public_path, "r") as f:
        print(f.read())


if __name__ == "__main__":
    main()
