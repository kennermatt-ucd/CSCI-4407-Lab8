"""
Task 7 – Plain (Textbook) RSA Demo
Implement raw RSA signing using modular exponentiation only — no hash, no padding.
  Sign:   S = M^d mod n
  Verify: M' = S^e mod n  →  check M' == M
Shows the math works, but exposes structural weaknesses exploited in Task 8.
"""

import os
from cryptography.hazmat.primitives import serialization

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
PRIV_PATH = os.path.join(BASE_DIR, "private_key.pem")


def load_rsa_components(priv_path: str):
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    priv_nums = private_key.private_numbers()
    pub_nums  = private_key.public_key().public_numbers()
    return pub_nums.n, pub_nums.e, priv_nums.d


def plain_rsa_sign(M: int, d: int, n: int) -> int:
    return pow(M, d, n)


def plain_rsa_verify(S: int, e: int, n: int) -> int:
    return pow(S, e, n)


def main():
    n, e, d = load_rsa_components(PRIV_PATH)

    # Use a small integer as the "message" for textbook RSA
    M = 42

    S  = plain_rsa_sign(M, d, n)
    M2 = plain_rsa_verify(S, e, n)

    print("=== Task 7: Plain (Textbook) RSA ===\n")
    print(f"Message integer M : {M}")
    print(f"Signature S       : {str(S)[:40]}...  (truncated)")
    print(f"Recovered M'      : {M2}")
    print(f"M' == M           : {M2 == M}")
    print("\nNote: the math is correct, but no hashing or padding means")
    print("this scheme is vulnerable to the forgery shown in Task 8.")


if __name__ == "__main__":
    main()
