"""
Task 8 – RSA Forgery (Multiplicative Attack)
Plain RSA is multiplicatively homomorphic:
  S(m1) * S(m2) mod n  =  S(m1 * m2 mod n)

Given two valid signed pairs (m1, s1) and (m2, s2), an attacker
can construct a valid signature for m1*m2 mod n without the private key.
"""

import os
from cryptography.hazmat.primitives import serialization
from task7_plain_rsa import plain_rsa_sign, plain_rsa_verify

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
PRIV_PATH = os.path.join(BASE_DIR, "private_key.pem")


def load_rsa_components(priv_path: str):
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    priv_nums = private_key.private_numbers()
    pub_nums  = private_key.public_key().public_numbers()
    return pub_nums.n, pub_nums.e, priv_nums.d


def main():
    n, e, d = load_rsa_components(PRIV_PATH)

    # Legitimate signer produces two signed messages
    m1, m2 = 6, 7
    s1 = plain_rsa_sign(m1, d, n)
    s2 = plain_rsa_sign(m2, d, n)

    # Attacker combines signatures — no private key used beyond this point
    m_forged = (m1 * m2) % n
    s_forged = (s1 * s2) % n

    # Verify the forged pair
    recovered = plain_rsa_verify(s_forged, e, n)
    forgery_valid = (recovered == m_forged)

    print("=== Task 8: RSA Forgery ===\n")
    print(f"m1 = {m1}, s1 = {str(s1)[:30]}...")
    print(f"m2 = {m2}, s2 = {str(s2)[:30]}...")
    print()
    print(f"Forged target message  : m1 * m2 mod n = {m_forged}")
    print(f"Forged signature       : s1 * s2 mod n = {str(s_forged)[:30]}...")
    print(f"Recovered from s_forged: {recovered}")
    print(f"Forgery valid?         : {forgery_valid}")
    print("\nConclusion: the attacker produced a valid (message, signature)")
    print("pair without ever accessing the private key.")


if __name__ == "__main__":
    main()
