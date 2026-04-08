"""
Task 4 – Message Tampering
Modify message1.txt and attempt to verify the original signature.
Demonstrates that any change to the message invalidates the signature.
"""

import os
from task3_sign_verify import load_public_key, verify_signature

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH  = os.path.join(BASE_DIR, "messages", "message1.txt")
SIG_PATH  = os.path.join(BASE_DIR, "message1.sig")
PUB_PATH  = os.path.join(BASE_DIR, "public_key.pem")

TAMPERING_ATTEMPTS = [
    b"Authorize transfer of $9000 to Eve's account ending in 0000.\n",
    b"Authorize transfer of $500 to Bob's account ending in 4821. URGENT.\n",
    b"Revoke all access permissions immediately.\n",
]


def main():
    public_key = load_public_key(PUB_PATH)

    with open(SIG_PATH, "rb") as f:
        original_signature = f.read()

    with open(MSG_PATH, "rb") as f:
        original_message = f.read()

    print("=== Task 4: Message Tampering ===\n")
    print(f"Original message  : {original_message.decode().strip()}")
    print(f"Original sig valid: {verify_signature(public_key, original_message, original_signature)}\n")
    print("-" * 60)

    for i, tampered_message in enumerate(TAMPERING_ATTEMPTS, start=1):
        result = verify_signature(public_key, tampered_message, original_signature)
        print(f"Attempt {i}: {tampered_message.decode().strip()}")
        print(f"  Verification: {'VALID' if result else 'INVALID'}\n")


if __name__ == "__main__":
    main()
