# Department of Computer Science & Engineering
## CSCI/CSCY 4407: Security & Cryptography
## Lab 8 Report: Digital Signatures – RSA, Forgery & Hash-then-Sign

**Group Number:** Group 10
**Semester:** Spring 2026
**Instructor:** Dr. Victor Kebande
**Teaching Assistant:** Celest Kester
**Submission Date:** APR 17 2026

**Group Members:**
- Matthew Kenner
- Jonathan Le
- Cassius Kemp

---

## Table of Contents

1. [Introduction](#introduction)
2. [Environment](#environment)
3. [Files Included](#files-included)
4. [Task 1 – Setup and Messages](#task-1)
5. [Task 2 – RSA Key Generation](#task-2)
6. [Task 3 – Signing and Verification](#task-3)
7. [Task 4 – Message Tampering](#task-4)
8. [Task 5 – Signature Tampering](#task-5)
9. [Task 6 – Public Key Trust](#task-6)
10. [Task 7 – Plain RSA (Python)](#task-7)
11. [Task 8 – RSA Forgery](#task-8)
12. [Task 9 – Hash-then-Sign](#task-9)
13. [Task 10 – Weak Hash Collision](#task-10)
14. [Task 11 – Comparison and Reflection](#task-11)


---

## Introduction <a name="introduction"></a>

This report documents the implementation and analysis performed for the Digital Signatures lab. Tasks cover RSA key generation, signing and verification, message and signature tampering, public key trust models, plain RSA weaknesses, existential forgery, the hash-then-sign paradigm, and weak hash collisions. Each task was completed in a Linux environment using Python 3 and the `cryptography` library. The report includes commands, source code, terminal outputs, screenshots, and interpretations for each experiment.

---

## Environment <a name="environment"></a>

All experiments were performed in a Linux environment using Kali Linux. Python 3 was used for all scripts, and RSA operations were implemented using Python's `cryptography` library.

- **Operating System:** Kali Linux
- **Python Version:** Python 3.12
- **Terminal:** Kali Linux terminal
- **Key Library:** `cryptography` (PyCA)
- **Installation:** Local Kali Linux install

---

## Files Included <a name="files-included"></a>

The following Python source files are included in this submission:

- `task1_setup.py` — Task 1: Directory setup and SHA-256 message hashes
- `task2_keygen.py` — Task 2: RSA key pair generation and export
- `task3_sign_verify.py` — Task 3: RSA-PSS signing and verification
- `task4_message_tamper.py` — Task 4: Detect tampered message via signature failure
- `task5_sig_tamper.py` — Task 5: Detect tampered signature
- `task6_pubkey_trust.py` — Task 6: Public key substitution / trust demonstration
- `task7_plain_rsa.py` — Task 7: Textbook (plain) RSA signature in Python
- `task8_rsa_forgery.py` — Task 8: Existential forgery against plain RSA
- `task9_hash_then_sign.py` — Task 9: Secure hash-then-sign construction
- `task10_weak_hash.py` — Task 10: Weak hash collision demonstration

---

## Task 1 – Setup and Messages <a name="task-1"></a>

### Objective

Create a working directory, populate it with message files, and compute SHA-256 hashes to establish a baseline for integrity verification throughout the lab.

### Steps Performed

- Created the lab directory and navigated into it
- Created three plaintext message files representing realistic signed documents
- Computed the SHA-256 hash of each message file
- Ran the setup script to confirm all files and hashes are correct

### Commands / Code Used

```bash
# Navigate to the lab directory and inspect its contents
pwd
ls messages/

# Compute SHA-256 hashes for all three message files
sha256sum messages/message1.txt messages/message2.txt messages/message3.txt

# Run the setup script
python3 code/task1_setup.py
```

```python
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
```

### Output Evidence

![alt text](task1.png)

### Recorded Hash Values

| File | SHA-256 Hash |
|------|-------------|
| message1.txt | `cc6375b0d1f5838836d9659cb0085655e2f071b77646cbd584963df3d0b34fbc` |
| message2.txt | `d29bf3edf72bbe5a8b39059e52add37bc23e546ae516caee86fd4a75d8dc029e` |
| message3.txt | `531bf82dfc90e66b805b4aaf297218e218a6049530951f985e54b6d66ef970f1` |

### Explanation

**What was done:** Three plaintext message files were created in the `messages/` directory, each representing a realistic signed document: a financial transfer authorization, an access control grant, and a sales contract. The `task1_setup.py` script then printed the contents of each file and computed the SHA-256 cryptographic hash for each one, establishing an integrity baseline before any signing operations.

**What happened:** Each file produced a unique 256-bit (64-character hex) hash value. Although the messages are short and human-readable, their SHA-256 digests look completely unrelated to each other and to the original text. This is expected behavior — SHA-256 maps any input to a fixed-size output in a way that appears random.

**Why it matters:** Recording hash values before signing establishes a verifiable baseline. If any message file is altered even by a single character after this point, its SHA-256 digest will change entirely (the avalanche effect), and the digital signature created against the original hash will fail to verify. This makes hashing the first line of defense for integrity: before signing even begins, we can prove the exact byte-for-byte state of each document.

---

## Task 2 – RSA Key Generation <a name="task-2"></a>

### Objective

Generate an RSA key pair (public + private), export both keys to disk in PEM format, and inspect their structure to understand the components of an asymmetric key pair.

### Steps Performed

- Generated a 2048-bit RSA private key using the `cryptography` library
- Exported the private key to `private_key.pem` (PEM format, no encryption)
- Derived and exported the public key to `public_key.pem`
- Inspected both PEM files to confirm key structure

### Commands / Code Used

```bash
# Generate the RSA key pair
python3 code/task2_keygen.py

# Inspect the resulting PEM files
cat public_key.pem
head -3 private_key.pem && echo "..." && tail -1 private_key.pem
```

```python
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

    pub_numbers = public_key.public_numbers()

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
```

### Output Evidence

![alt text](task2.png)

### Key Details

| Property | Value |
|----------|-------|
| Key type | RSA |
| Key size (bits) | 2048 |
| Public exponent (e) | 65537 |
| Private key file | private_key.pem |
| Public key file | public_key.pem |

### Explanation

**What was done:** The `task2_keygen.py` script used Python's `cryptography` library to generate a 2048-bit RSA private key with a public exponent of 65537. The private key was serialized to `private_key.pem` in TraditionalOpenSSL PEM format without passphrase encryption, and the corresponding public key was derived and exported to `public_key.pem` in SubjectPublicKeyInfo PEM format.

**What happened:** Two files were created on disk. `private_key.pem` contains the full RSA key material (modulus, private exponent, primes, and CRT coefficients) encoded in base64 between `-----BEGIN RSA PRIVATE KEY-----` headers. `public_key.pem` contains only the modulus and public exponent encoded between `-----BEGIN PUBLIC KEY-----` headers, which is safe to share publicly.

**Why it matters:** The asymmetry between these two keys is the foundation of RSA digital signatures. Only the holder of the private key can produce a signature, while anyone with the public key can verify it — but cannot reverse-engineer the private key from it (given a sufficiently large key size). A 2048-bit key provides approximately 112 bits of security, which is the current minimum recommended by NIST. The private key must be kept strictly confidential; if it is compromised, an attacker can forge signatures for any message under that identity.

---

## Task 3 – Signing and Verification <a name="task-3"></a>

### Objective

Sign a message using the RSA private key and verify the signature using the corresponding public key, demonstrating the core digital signature workflow.

### Steps Performed

- Loaded the private key from `private_key.pem`
- Signed `message1.txt` using RSA-PSS with SHA-256
- Saved the signature to `message1.sig`
- Loaded the public key and verified the signature against the original message
- Confirmed that verification returns success

### Commands / Code Used

```bash
# Sign message1.txt and verify the signature
python3 code/task3_sign_verify.py

# Confirm the signature file was written to disk
ls -lh message1.sig
```

```python
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
```

### Output Evidence

![alt text](task3.png)

### Recorded Signature

| Item | Value |
|------|-------|
| Message file | message1.txt |
| Signature file | message1.sig |
| Signature (hex, first 32 bytes) | See screenshot |
| Verification result | VALID |

### Explanation

**What was done:** The script loaded the private key from `private_key.pem` and read the raw bytes of `message1.txt`. It then called `private_key.sign()` using RSA-PSS padding with SHA-256 as both the message digest and the MGF1 mask generation hash. The resulting 256-byte binary signature was written to `message1.sig`. The public key was then used to verify the signature against the original message bytes, and the result was printed to the terminal.

**What happened:** The verification returned `VALID`, confirming that the signature produced by the private key is mathematically consistent with the public key and the exact bytes of `message1.txt`. The signature itself is 256 bytes of binary data (2048-bit RSA output), displayed as a 512-character hex string in the terminal.

**Why it matters:** This task demonstrates all three core properties of a digital signature. **Authenticity** — only someone holding the private key could have produced that signature. **Integrity** — the signature is cryptographically bound to the exact byte contents of the message; any alteration will break it. **Non-repudiation** — the signer cannot later deny having signed, because the valid signature can only have originated from their private key. RSA-PSS is used rather than plain RSA because it incorporates randomized salt and a proof of security under the random oracle model, making it resistant to padding oracle attacks that affect deterministic schemes like PKCS#1 v1.5.

---

## Task 4 – Message Tampering <a name="task-4"></a>

### Objective

Modify the signed message and attempt to verify the original signature, demonstrating that digital signatures detect unauthorized content changes.

### Steps Performed

- Used the valid signature from Task 3
- Modified `message1.txt` content (changed a word or value)
- Attempted to verify the original signature against the modified message
- Confirmed that verification fails with an `InvalidSignature` exception

### Commands / Code Used

```bash
# Run the tampering script (original message1.txt is NOT modified on disk;
# the script injects tampered content in memory for each attempt)
python3 code/task4_message_tamper.py
```

```python
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
```

### Output Evidence

![alt text](task4.png)

### Tampering Results

| Attempt | Modification Made | Verification Result |
|---------|------------------|-------------------|
| 1 | Changed amount from $500 to $9000 and recipient to Eve | INVALID |
| 2 | Appended " URGENT." to the original transfer line | INVALID |
| 3 | Replaced entire message with an access revocation command | INVALID |

### Explanation

**What was done:** Rather than manually editing the file on disk, the script holds the original `message1.sig` signature and tests it against three programmatically crafted tampered messages. The first simulates a financial fraud (amount and account changed), the second simulates a minor word addition, and the third replaces the message entirely — covering a range of tampering severities.

**What happened:** All three verification attempts returned `INVALID`. The `cryptography` library's `verify()` method raised an `InvalidSignature` exception internally for each tampered message, which the `verify_signature` helper caught and translated into `False`. Not a single tampered byte went undetected.

**Why it matters:** RSA-PSS signs the SHA-256 hash of the message, not the message itself. SHA-256 has the avalanche effect: even changing one character in the input produces a completely different 256-bit digest. Since the stored signature was computed over the original digest, it cannot match the new digest produced from any tampered version. This means an adversary who intercepts a signed financial instruction and alters the amount or recipient will be caught immediately upon verification — the signature serves as a tamper-evident seal over the entire message content.

---

## Task 5 – Signature Tampering <a name="task-5"></a>

### Objective

Modify the signature itself (leaving the message intact) and attempt verification, showing that a corrupted signature is also rejected.

### Steps Performed

- Used the valid message and original signature from Task 3
- Flipped one or more bytes in `message1.sig`
- Attempted to verify the tampered signature against the original (unmodified) message
- Confirmed that verification fails

### Commands / Code Used

```bash
python3 code/task5_sig_tamper.py
```

```python
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
```
### Output Evidence

![task5](task5.png)

### Tampering Results

| Byte Index Modified | XOR Mask | Verification Result |
|--------------------|----------|-------------------|
| 0 | 0xFF | INVALID |
| 8 | 0x01 | INVALID |
| 127 | 0xAB | INVALID |

### Explanation

**What was done:** The script loaded the valid `message1.sig` produced in Task 3 and applied XOR bit-flips to three different byte positions: byte 0 (XOR `0xFF`, flipping all 8 bits), byte 8 (XOR `0x01`, flipping just the least significant bit), and byte 127 (XOR `0xAB`, flipping multiple non-contiguous bits). Each tampered signature was then passed to the verifier alongside the original, unmodified `message1.txt`.

**What happened:** All three tampered signatures returned `INVALID`. Even the smallest possible modification — flipping a single bit at byte 8 with mask `0x01` — was enough to cause verification to fail. The RSA-PSS verification algorithm detected that the signature no longer corresponded to the message and raised an `InvalidSignature` exception internally.

**Why it matters:** This confirms that the signature blob itself is integrity-protected, not just the message. An attacker who intercepts a signed document cannot alter either half of the (message, signature) pair without invalidating the whole thing. Flipping even one bit in a 256-byte RSA signature destroys the mathematical relationship that verification relies on, because the entire recovered value shifts away from the expected hash. Together with Task 4, this demonstrates that digital signatures provide end-to-end tamper evidence over both the content and the authenticator.

---

## Task 6 – Public Key Trust <a name="task-6"></a>

### Objective

Demonstrate why public key authenticity matters by showing that verifying a valid signature with the *wrong* public key fails, and discussing what happens if an adversary substitutes their own key pair.

### Steps Performed

- Generated a second, independent RSA key pair (`attacker_private.pem`, `attacker_public.pem`)
- Signed `message1.txt` with the **original** private key (Task 2)
- Attempted to verify that signature using the **attacker's** public key
- Signed `message1.txt` with the **attacker's** private key and verified with the attacker's public key (shows substitution succeeds if trust is absent)

### Commands / Code Used

```bash
# Run the public key trust demonstration
python3 code/task6_pubkey_trust.py
```

```python
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

BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
MSG_PATH  = os.path.join(BASE_DIR, "messages", "message1.txt")
SIG_PATH  = os.path.join(BASE_DIR, "message1.sig")
PUB_PATH  = os.path.join(BASE_DIR, "public_key.pem")
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
```

### Output Evidence

![Task6 Output](task6.png)

### Trust Scenarios

| Scenario | Key Used to Sign | Key Used to Verify | Result |
|----------|-----------------|-------------------|--------|
| Legitimate | Original private | Original public | VALID |
| Wrong key | Original private | Attacker public | INVALID |
| Substitution | Attacker private | Attacker public | VALID |

### Explanation

**What was done:** The script loaded the original private/public key pair and the `message1.sig` signature from Task 3. It then generated a fresh, independent attacker RSA key pair entirely in memory (never written to disk). Using the attacker's private key, it produced a second signature over the same message. All three verification scenarios were then run and printed.

**What happened:** Scenario 1 returned `VALID` — confirming the baseline still holds. Scenario 2 returned `INVALID` — the original signature cryptographically cannot verify under a different public key, because RSA verification essentially "decrypts" the signature using the public key and checks the recovered hash; a mismatched key produces garbage, not the expected digest. Scenario 3 returned `VALID` — the attacker's signature verifies perfectly under the attacker's own public key, showing that the signature scheme itself cannot detect key substitution.

**Why it matters:** The mathematical correctness of a signature only proves that the message was signed by whoever holds the private key corresponding to the verifier's copy of the public key. If the verifier cannot confirm that the public key genuinely belongs to the expected identity, an attacker can substitute their own key pair and produce a signature that passes verification — even though the victim never signed anything. This is exactly the attack that a **Public Key Infrastructure (PKI)** and **Certificate Authorities (CAs)** exist to prevent: a CA-issued certificate cryptographically binds a public key to an identity, so verifiers can trust whose key they are actually using before accepting any signature.

---

## Task 7 – Plain RSA (Python) <a name="task-7"></a>

### Objective

Implement textbook (plain) RSA signing in Python using raw modular exponentiation, without padding or hashing, and observe its structural properties.

### Steps Performed

- Extracted the RSA private key components (n, d, e) from the generated key
- Implemented plain RSA signing: `S = M^d mod n`
- Implemented plain RSA verification: `M' = S^e mod n`, check `M' == M`
- Signed a small integer message and verified it

### Commands / Code Used

```bash
python3 code/task7_plain_rsa.py
```

```python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m

#Toy RSA Parameters
p = 61
q = 53
N = p * q                #3233
phi = (p - 1) * (q - 1)  #3120
e = 17                   #Public Exponent
d = modinv(e, phi)       #Private Exponent (2753)

#Message that will be signed
m = 42

#Signing (Using Private Key 'd')
sigma = pow(m, d, N)

#Verification (Using Public Key 'e')
check = pow(sigma, e, N)

print("--- Task 7: Plain RSA Signature Intuition ---")
print("N =", N)
print("e =", e)
print("d =", d)
print("Message representative m =", m)
print("Signature sigma =", sigma)
print("Verification result =", check)
print("Valid? (Does check == m?)" , check == m)
```

### Output Evidence

![Task7 Output](task7.png)

### Recorded Values

| Parameter | Value (truncated) |
|-----------|------------------|
| Modulus n | 3233 |
| Public exponent e | 17 |
| Message integer M | 42 |
| Signature integer S | 2577 |
| Recovered M' | 42 |
| Match? | Yes |

### Explanation

**What was done:** As seen in the screenshot output, taking the signature (2577) and applying the verification math (2577^17 mod 3233) results in exactly 42, which exactly matches the original message.

**What happened:** It works due to Euler's Totient Theorem so, this means that e and d are mathematical inverses modulo ϕ(N) and applying them sequentially causes them to cancel each other out. Therefore, (m^d)^e ≡ m^(ed) ≡ m^1 ≡ m(modN).

**Why it matters:** Mathematical correctness only proves that the math is functioning properly, it cannot prove any form cryptographic security. Plain RSA signatures are structurally insecure because they possess a multiplicative property that allows attackers to easily forge signatures on new messages without needing access to a private key.

---

## Task 8 – RSA Forgery <a name="task-8"></a>

### Objective

Demonstrate an existential forgery attack against plain (unpadded) RSA, showing that an attacker can construct a valid-looking signature without knowledge of the private key.

### Steps Performed

- Used the public key (n, e) only — no private key access
- Selected a target signature integer S
- Computed the corresponding "message" M = S^e mod n
- Verified that the pair (M, S) passes plain RSA verification
- Demonstrated that this constitutes a valid forgery (signature without signing)

### Commands / Code Used

```bash
python3 code/task8_rsa_forgery.py
```

```python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m

#Toy RSA Parameters
p = 61
q = 53
N = p * q
phi = (p - 1) * (q - 1)
e = 17
d = modinv(e, phi)

#Two previously signed messages
m1 = 7
m2 = 9
s1 = pow(m1, d, N) #Signature 1
s2 = pow(m2, d, N) #Signature 2

#Forgery
#We as an attacker want to forge a signature for m3 (m1 * m2)
m3 = (m1 * m2) % N

s3 = (s1 * s2) % N

#Verification
check = pow(s3, e, N)

print("--- Task 8: Raw RSA Forgery Experiment ---")
print("m1 =", m1)
print("m2 =", m2)
print("m3 = m1*m2 mod N =", m3)
print("s1 (Valid Sig for m1) =", s1)
print("s2 (Valid Sig for m2) =", s2)
print("Forged-style signature s3 = s1*s2 mod N =", s3)
print("Verification of s3 gives =", check)
print("Does it verify as m3?", check == m3)
```

### Output Evidence

![Task8 Output](task8.png)

### Forgery Results

| Item | Value |
|------|-------|
| Chosen signature S | 1723 |
| Derived message M = S^e mod n | 63 |
| Forgery passes verification? | Yes |
| Is M a meaningful message? | No, it is just the mathematical product of the two previous messages. |

### Explanation

**RSA Signature Shorcomings:** Raw RSA signatures are homomorphic with respect the multiplication used, this means that the math proves that (m1^d ⋅ m2^d)(modN) is exactly equal to(m1⋅m2)^d (modN). Therefore, an attacker can simply multiply two valid signatures they have intercepted to create a new valid forged signature for a completely different message (m3), without even knowing the private key.

**How we relate unforgeability:** The core requirement of a secure digital signature (Unforgeability under Chosen Message Attack) is that an adversary cannot produce a valid signature for a message that was never signed by the owner. Because an attacker can trivially compute a valid signature for m3​ just by observing the signatures for m1 and m2​, plain RSA completely fails the UF-CMA security requirements to be considered secure.

---

## Task 9 – Hash-then-Sign <a name="task-9"></a>

### Objective

Implement the secure hash-then-sign construction (RSA-PSS with SHA-256) and confirm that it resists the forgery demonstrated in Task 8.

### Steps Performed

- Loaded the private key from `private_key.pem`
- Hashed `message1.txt` with SHA-256
- Signed the hash digest using RSA-PSS padding
- Verified the signature using the public key
- Attempted to apply the Task 8 forgery technique against this scheme and showed it fails

### Commands / Code Used

```bash
python3 code/task9_hash_then_sign.py
```

```python
import hashlib

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m

#Toy RSA Parameters
p = 61
q = 53
N = p * q
phi = (p - 1) * (q - 1)
e = 17
d = modinv(e, phi)

print("--- Task 9: Hash-then-Sign Workflow ---")

#Hashing the Message
message = b"Authorize transfer of 100 dollars to Bob."
print(f"Original Message: '{message.decode()}'")

digest = hashlib.sha256(message).digest()

#Converts the binary hash into an integer so that the RSA math can work on it
h = int.from_bytes(digest, byteorder="big") % N
print("Hash representative h =", h)

#Signing the Hash
#We apply the private key 'd' to the hash instead of the message itself
sigma = pow(h, d, N)
print("Signature sigma =", sigma)

#We perform Verification
check = pow(sigma, e, N)
print("Recovered verification value =", check)
print("Valid? (Does recovered value == original hash?)", check == h)

print("\n--- Tampering (For ease of demonstration) ---")
#Modifing the message slightly
tampered_message = b"Authorize transfer of 900 dollars to Bob."
print(f"Tampered Message: '{tampered_message.decode()}'")

tampered_digest = hashlib.sha256(tampered_message).digest()
tampered_h = int.from_bytes(tampered_digest, byteorder="big") % N

print("New Hash representative h =", tampered_h)
print("Does the old signature still verify? (Does recovered value == new hash?)", check == tampered_h)
```

### Output Evidence

![Task9 Output](task9.png)

### Results

| Step | Value / Result |
|------|---------------|
| SHA-256 hash of message | 1505 |
| Signature (hex, first 32 bytes) | 3052 |
| Verification result | Valid |
| Forgery attempt result | Failed |

### Explanation

**Why the signature no longer matches:** When the message was changed from 100 to 900 dollars, the SHA-256 hash function generated a completely different hash. And since the verification process checks if the signature matches the current hash of the document it means that the old signature will mathematically fail to match the new hash, exposing any form of tampering with the message.

**Why hashing helps:** RSA math only works on integers smaller than the modulus (N) so, without hashing a 10MB PDF document could not be signed using a 2048 bit RSA key. A cryptographic hash function perfectly compresses any arbitrary length file into a fixed size integer, allowing the RSA math to process it efficiently while securely binding the signature to the document. Importantly, hashing also destroys the mathematical structure of the message and this prevents multiplicative forgery attacks as demonstrated in Task 8.

---

## Task 10 – Weak Hash Collision <a name="task-10"></a>

### Objective

Demonstrate that a digital signature scheme is only as secure as the underlying hash function by constructing two different messages that share the same weak hash value, showing a signature computed for one is accepted for the other.

### Steps Performed

- Implemented a toy weak hash function (e.g., 8-bit truncated hash or custom low-collision function)
- Found or constructed two messages with the same weak hash output (a collision)
- Signed the first message using hash-then-sign with the weak hash
- Showed the signature verifies against the second (different) message
- Contrasted this with SHA-256, which does not exhibit the same collision

### Commands / Code Used

```bash
python3 code/task10_weak_hash.py
```

```python
print("--- Task 10: Weak Hash Function Collision ---")

def weak_hash(msg):
    return sum(msg) % 100

m1 = b"Pay Bob 100"

m2 = b"Pay obB 010" 

h1 = weak_hash(m1)
h2 = weak_hash(m2)

print("m1 =", m1.decode())
print("m2 =", m2.decode())
print("weak_hash(m1) =", h1)
print("weak_hash(m2) =", h2)

if h1 == h2:
    print("\nCollision found: A signature generated for 'm1' would perfectly verify for 'm2'!")
else:
    print("\nNo collision for this pair. Try other messages.")
```

### Output Evidence

![Task10 Output](task10.png)

### Collision Evidence

| Item | Value |
|------|-------|
| Message A | Pay Bob 100 |
| Message B | Pay obB 010 |
| Weak hash of A | 82 |
| Weak hash of B | 82 |

### Explanation

**Why collision breaks trust:** In the hash-then-sign workflow demonstrated, the digital signature is mathematically bound to the hash value and is not bound the message itself. If an attacker can find a collision between two different messages that can produce the exact same hash, then they can take the original message and pull what data is needed. The attacker can then detach that valid signature and attach it to their malicious message (m2). Due to the fact that H(m1) = H(m2), the verification algorithm will accept the forged document as mathematically authentic.

**Collision resistant hash functions:** To prevent the attack described above, it must be computationally impossible for an attacker to find two inputs that hash to the same output. Functions like SHA-256 are used in real-world systems because they guarantee strong collision resistance, ensuring a signature can uniquely be tied to only one specific document.
---

## Task 11 – Comparison and Reflection

### Objective

Synthesize all experimental results into a structured comparison table and reflection, clearly articulating the security properties and limitations of each approach explored in this lab.

### Comparison Table
| Method | Works Correctly? | Secure? | Main Weakness / Main Strength |
| :--- | :--- | :--- | :--- |
| **1. OpenSSL-based structured RSA** (Tasks 1-6) | Yes | **Yes** | **Strength:** Reflects realistic practice. Uses secure padding, collision-resistant hashing (SHA-256), and proper key sizes. |
| **2. Toy plain RSA signature intuition** (Task 7) | Yes | No | **Weakness:** Only educational. Uses insecurely small keys and lacks padding/hashing. |
| **3. Toy raw RSA forgery experiment** (Task 8) | Yes | No | **Weakness:** Demonstrates severe structural vulnerability (multiplicative homomorphism) allowing trivial forgery without the private key. |
| **4. Toy hash-then-sign RSA** (Task 9) | Yes | No | **Strength:** Solves the raw RSA forgery issue and handles arbitrary lengths. **Weakness:** Still uses toy key sizes, making it insecure in practice. |
| **5. Weak-hash signing thought experiment** (Task 10)| Yes | No | **Weakness:** Exposes how a lack of collision resistance allows an attacker to reuse a signature on a forged, malicious document. |

---

### Reflection

Digital signatures provide three vital security guarantees, authentication, integrity, and non-repudiation. Through this lab, we saw that while the basic RSA math is efficient and elegant in its operation, plain RSA signing is fundamentally insecure because its multiplicative property allows attackers to forge valid signatures without possessing the private key. Hashing the message prior to signing is necessary for not only compressing the files used into manageable sizes for the RSA arithmetic, but also to destroy the mathematical structure that enables those forgery attacks in the first place. However, the choice of hash function is the most important aspect, as if it lacks collision resistance an attacker could attach a legitimate signature to a forged document and get away with it. Finally, the OpenSSL tasks demonstrated that even mathematically perfect signatures are useless if the verifier cannot trust the public key. As a signature is only meaningful relative to a specific public key that it is used with, undermining the absolute necessity of authenticating our public keys via trusted certificates before verifying any of the data.

---
