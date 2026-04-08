"""
Task 10 – Weak Hash Collision
Implement a deliberately weak 8-bit hash function (truncated CRC-style).
Find two different messages that share the same weak hash value.
Sign message A; show the signature also verifies for message B.
Contrast with SHA-256, which produces distinct digests for both messages.
"""

import hashlib
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


def weak_hash(message: bytes) -> int:
    """
    Deliberately weak 8-bit hash: XOR all bytes of the SHA-256 digest.
    Only 256 possible output values — collisions are trivial to find.
    """
    digest = hashlib.sha256(message).digest()
    result = 0
    for byte in digest:
        result ^= byte
    return result  # 0–255


def find_collision(base_message: bytes) -> bytes:
    """Brute-force a second message with the same weak hash as base_message."""
    target = weak_hash(base_message)
    counter = 0
    while True:
        candidate = f"Collision candidate #{counter}".encode()
        if weak_hash(candidate) == target and candidate != base_message:
            return candidate
        counter += 1


def main():
    n, e, d = load_rsa_components(PRIV_PATH)

    message_a = b"Authorize transfer of $500 to Bob."
    message_b = find_collision(message_a)

    hash_a = weak_hash(message_a)
    hash_b = weak_hash(message_b)

    # Sign message A using the weak hash
    sig = plain_rsa_sign(hash_a, d, n)

    # Verify signature against message B (collision attack)
    recovered = plain_rsa_verify(sig, e, n)
    collision_succeeds = (recovered == hash_b)

    print("=== Task 10: Weak Hash Collision ===\n")
    print(f"Message A       : {message_a.decode()}")
    print(f"Message B       : {message_b.decode()}")
    print(f"Weak hash A     : {hash_a}")
    print(f"Weak hash B     : {hash_b}")
    print(f"Hashes match    : {hash_a == hash_b}")
    print()
    print(f"Signature of A verifies for B: {collision_succeeds}")
    print()
    print("SHA-256 comparison:")
    print(f"  SHA-256(A)    : {hashlib.sha256(message_a).hexdigest()}")
    print(f"  SHA-256(B)    : {hashlib.sha256(message_b).hexdigest()}")
    print(f"  Match         : {hashlib.sha256(message_a).digest() == hashlib.sha256(message_b).digest()}")
    print("\nConclusion: collision resistance is a required property for secure")
    print("hash-then-sign schemes. SHA-256 provides this; the 8-bit hash does not.")


if __name__ == "__main__":
    main()
