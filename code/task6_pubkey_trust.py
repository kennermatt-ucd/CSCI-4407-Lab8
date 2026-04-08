"""
Task 6 – Public Key Trust
Generate a second "attacker" key pair and demonstrate:
  1. Original signature fails when verified with the attacker's public key.
  2. Attacker's own signature verifies with their own public key (substitution scenario).
Shows why public key authenticity is essential.
"""

import os
from task2_keygen import generate_rsa_keypair
from task3_sign_verify import (
    load_private_key, load_public_key,
    sign_message, verify_signature,
)

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH = os.path.join(BASE_DIR, "messages", "message1.txt")
SIG_PATH = os.path.join(BASE_DIR, "message1.sig")
PUB_PATH = os.path.join(BASE_DIR, "public_key.pem")
PRIV_PATH = os.path.join(BASE_DIR, "private_key.pem")


def main():
    # Load original keys and signature
    original_priv = load_private_key(PRIV_PATH)
    original_pub  = load_public_key(PUB_PATH)

    with open(MSG_PATH, "rb") as f:
        message = f.read()

    with open(SIG_PATH, "rb") as f:
        original_sig = f.read()

    # Generate attacker key pair (in memory only)
    attacker_priv, attacker_pub = generate_rsa_keypair()
    attacker_sig = sign_message(attacker_priv, message)

    print("=== Task 6: Public Key Trust ===\n")

    # Scenario 1: Correct key pair
    result1 = verify_signature(original_pub, message, original_sig)
    print(f"Scenario 1 – Legitimate (original sig + original pub key): {'VALID' if result1 else 'INVALID'}")

    # Scenario 2: Wrong public key
    result2 = verify_signature(attacker_pub, message, original_sig)
    print(f"Scenario 2 – Original sig verified with ATTACKER public key: {'VALID' if result2 else 'INVALID'}")

    # Scenario 3: Attacker signs with their own key → verifies with their own key
    result3 = verify_signature(attacker_pub, message, attacker_sig)
    print(f"Scenario 3 – Attacker sig verified with attacker public key: {'VALID' if result3 else 'INVALID'}")

    print("\nConclusion: if Alice accepts any public key without verification,")
    print("an attacker can substitute their own key pair and forge valid signatures.")


if __name__ == "__main__":
    main()
