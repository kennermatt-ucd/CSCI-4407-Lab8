"""
Task 5 – Signature Tampering
Flip bytes in the signature while leaving the message untouched.
Demonstrates that a corrupted signature is also rejected.
"""

import os
from task3_sign_verify import load_public_key, verify_signature

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH = os.path.join(BASE_DIR, "messages", "message1.txt")
SIG_PATH = os.path.join(BASE_DIR, "message1.sig")
PUB_PATH = os.path.join(BASE_DIR, "public_key.pem")

TAMPER_TARGETS = [
    (0,   0xFF),
    (8,   0x01),
    (127, 0xAB),
]


def tamper_signature(signature: bytes, byte_index: int, xor_mask: int) -> bytes:
    sig = bytearray(signature)
    sig[byte_index] ^= xor_mask
    return bytes(sig)


def main():
    public_key = load_public_key(PUB_PATH)

    with open(MSG_PATH, "rb") as f:
        message = f.read()

    with open(SIG_PATH, "rb") as f:
        original_sig = f.read()

    print("=== Task 5: Signature Tampering ===\n")
    print(f"Original sig valid: {verify_signature(public_key, message, original_sig)}\n")
    print("-" * 60)

    for i, (index, mask) in enumerate(TAMPER_TARGETS, start=1):
        tampered = tamper_signature(original_sig, index, mask)
        result   = verify_signature(public_key, message, tampered)
        print(f"Attempt {i}: flip byte[{index}] XOR 0x{mask:02X}")
        print(f"  Verification: {'VALID' if result else 'INVALID'}\n")


if __name__ == "__main__":
    main()
