"""
Task 1 – Setup and Messages
Display the working directory, list message files, print their contents,
and compute SHA-256 hashes to establish an integrity baseline.
"""

import hashlib
import os

MESSAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "messages")


def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    print("=== Task 1: Setup and Messages ===\n")
    print(f"Working directory: {os.path.abspath(MESSAGE_DIR)}\n")

    files = sorted(
        f for f in os.listdir(MESSAGE_DIR) if f.endswith(".txt")
    )

    for filename in files:
        path = os.path.join(MESSAGE_DIR, filename)
        with open(path, "r") as f:
            content = f.read().strip()
        digest = sha256_file(path)
        print(f"File    : {filename}")
        print(f"Content : {content}")
        print(f"SHA-256 : {digest}")
        print()


if __name__ == "__main__":
    main()
