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
15. [Appendix – Python Scripts](#appendix)
16. [Pre-Submission Checklist](#checklist)

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
- `task2_rsa_keygen.py` — Task 2: RSA key pair generation and export
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
# [INSERT COMMANDS HERE — e.g., mkdir, cd, pwd, ls, sha256sum]
```

```python
# [CODE HERE — task1_setup.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task1_directory_setup.png]**
> Show: terminal output of directory creation, `ls` listing all message files.

> **[INSERT SCREENSHOT HERE — task1_hashes.png]**
> Show: SHA-256 hash output for all three message files.

### Recorded Hash Values

| File | SHA-256 Hash |
|------|-------------|
| message1.txt | [INSERT HASH] |
| message2.txt | [INSERT HASH] |
| message3.txt | [INSERT HASH] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the directory structure created and the files used.]

**What happened:** [EXPLAIN HERE — describe the hash output observed.]

**Why it matters:** [EXPLAIN HERE — explain why establishing a hash baseline matters before signing, and what the avalanche effect demonstrates.]

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
# [INSERT COMMANDS HERE — e.g., python3 task2_rsa_keygen.py, cat public_key.pem]
```

```python
# [CODE HERE — task2_rsa_keygen.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task2_keygen_output.png]**
> Show: script execution output confirming key generation, key sizes, and file creation.

> **[INSERT SCREENSHOT HERE — task2_private_pem.png]**
> Show: contents of `private_key.pem` (first/last few lines — do NOT expose full private key).

> **[INSERT SCREENSHOT HERE — task2_public_pem.png]**
> Show: full contents of `public_key.pem`.

### Key Details

| Property | Value |
|----------|-------|
| Key type | RSA |
| Key size (bits) | [INSERT — e.g., 2048] |
| Public exponent (e) | [INSERT — e.g., 65537] |
| Private key file | private_key.pem |
| Public key file | public_key.pem |

### Explanation

**What was done:** [EXPLAIN HERE — describe the key generation process and parameters chosen.]

**What happened:** [EXPLAIN HERE — describe the PEM output and what each file contains.]

**Why it matters:** [EXPLAIN HERE — explain public/private key roles in digital signatures, why key size matters, and why the private key must be kept secret.]

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
# [INSERT COMMANDS HERE — e.g., python3 task3_sign_verify.py]
```

```python
# [CODE HERE — task3_sign_verify.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task3_sign_output.png]**
> Show: script output displaying the signature (hex) and confirmation of signing.

> **[INSERT SCREENSHOT HERE — task3_verify_success.png]**
> Show: verification output confirming "Signature is VALID."

### Recorded Signature

| Item | Value |
|------|-------|
| Message file | message1.txt |
| Signature file | message1.sig |
| Signature (hex, first 32 bytes) | [INSERT] |
| Verification result | [INSERT — e.g., VALID] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the signing and verification steps.]

**What happened:** [EXPLAIN HERE — describe the output and verification result.]

**Why it matters:** [EXPLAIN HERE — explain the asymmetric property: only the private key can sign, but anyone with the public key can verify. Discuss non-repudiation.]

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
# [INSERT COMMANDS HERE — e.g., nano message1.txt, python3 task4_message_tamper.py]
```

```python
# [CODE HERE — task4_message_tamper.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task4_modified_message.png]**
> Show: the modified message content via `cat message1.txt`.

> **[INSERT SCREENSHOT HERE — task4_verify_fail.png]**
> Show: script output displaying "Signature is INVALID" or the caught `InvalidSignature` error.

### Tampering Results

| Attempt | Modification Made | Verification Result |
|---------|------------------|-------------------|
| 1 | [DESCRIBE CHANGE] | [INSERT — INVALID] |
| 2 | [DESCRIBE CHANGE] | [INSERT — INVALID] |
| 3 | [DESCRIBE CHANGE] | [INSERT — INVALID] |

### Explanation

**What was done:** [EXPLAIN HERE — describe what modifications were made to the message.]

**What happened:** [EXPLAIN HERE — describe the verification failure and the exception raised.]

**Why it matters:** [EXPLAIN HERE — explain how the signature binds to the exact message bytes and why any change invalidates it. Connect to integrity protection.]

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
python3 task5_sig_tamper.py
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
        print(f"  Verification: {'VALID' if result else 'INVALID'}\n")```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task5_tampered_sig.png]**
> Show: script output displaying the original vs. tampered signature bytes and the verification failure.

### Tampering Results

| Byte Index Modified | XOR Mask | Verification Result |
|--------------------|----------|-------------------|
| [INSERT] | [INSERT] | [INSERT — INVALID] |
| [INSERT] | [INSERT] | [INSERT — INVALID] |
| [INSERT] | [INSERT] | [INSERT — INVALID] |

### Explanation

**What was done:** [EXPLAIN HERE — describe which bytes of the signature were flipped and how.]

**What happened:** [EXPLAIN HERE — describe the verification failure.]

**Why it matters:** [EXPLAIN HERE — explain that both the message and the signature are integrity-protected; an adversary cannot alter either without detection.]

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
# [INSERT COMMANDS HERE]
```

```python
# [CODE HERE — task6_pubkey_trust.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task6_wrong_key_fail.png]**
> Show: verification failure when the wrong public key is used.

> **[INSERT SCREENSHOT HERE — task6_substitution.png]**
> Show: attacker's signature verifying with attacker's public key (key substitution scenario).

### Trust Scenarios

| Scenario | Key Used to Sign | Key Used to Verify | Result |
|----------|-----------------|-------------------|--------|
| Legitimate | Original private | Original public | [INSERT] |
| Wrong key | Original private | Attacker public | [INSERT] |
| Substitution | Attacker private | Attacker public | [INSERT] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the key substitution experiment.]

**What happened:** [EXPLAIN HERE — describe each scenario's verification result.]

**Why it matters:** [EXPLAIN HERE — explain the role of a Public Key Infrastructure (PKI) or certificate authority (CA) in binding public keys to identities. Discuss why simply having a valid signature is insufficient without trusted key distribution.]

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
# [INSERT COMMANDS HERE — e.g., python3 task7_plain_rsa.py]
```

```python
# [CODE HERE — task7_plain_rsa.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task7_plain_rsa_output.png]**
> Show: script output with key components (n, e, d — or partial), computed signature integer, and verification result.

### Recorded Values

| Parameter | Value (truncated) |
|-----------|------------------|
| Modulus n (first 20 digits) | [INSERT] |
| Public exponent e | [INSERT] |
| Message integer M | [INSERT] |
| Signature integer S (first 20 digits) | [INSERT] |
| Recovered M' | [INSERT] |
| Match? | [INSERT — Yes/No] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the raw RSA operations performed.]

**What happened:** [EXPLAIN HERE — describe the output and whether M' matched M.]

**Why it matters:** [EXPLAIN HERE — explain that plain RSA without hashing or padding is deterministic and homomorphic, which enables forgery attacks. This motivates Tasks 8 and 9.]

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
# [INSERT COMMANDS HERE — e.g., python3 task8_rsa_forgery.py]
```

```python
# [CODE HERE — task8_rsa_forgery.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task8_forgery_output.png]**
> Show: forged signature integer, the derived "message," and the verification result confirming the forgery passes.

### Forgery Results

| Item | Value |
|------|-------|
| Chosen signature S | [INSERT] |
| Derived message M = S^e mod n | [INSERT — partial] |
| Forgery passes verification? | [INSERT — Yes/No] |
| Is M a meaningful message? | [INSERT — discuss] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the existential forgery construction.]

**What happened:** [EXPLAIN HERE — explain how the pair (M, S) was created and that it verifies correctly.]

**Why it matters:** [EXPLAIN HERE — explain that plain RSA is malleable: given (M₁, S₁) and (M₂, S₂), an attacker can construct a valid signature for M₁·M₂ mod n. This demonstrates why real RSA signatures always use a hash function and padding (e.g., PKCS#1 v1.5 or PSS).]

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
# [INSERT COMMANDS HERE — e.g., python3 task9_hash_then_sign.py]
```

```python
# [CODE HERE — task9_hash_then_sign.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task9_sign_output.png]**
> Show: computed SHA-256 hash, RSA-PSS signature (hex), and verification result.

> **[INSERT SCREENSHOT HERE — task9_forgery_fail.png]**
> Show: the Task 8 forgery technique failing against hash-then-sign (InvalidSignature or equivalent).

### Results

| Step | Value / Result |
|------|---------------|
| SHA-256 hash of message | [INSERT] |
| Signature (hex, first 32 bytes) | [INSERT] |
| Verification result | [INSERT — VALID] |
| Forgery attempt result | [INSERT — INVALID / rejected] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the hash-then-sign construction and why hashing is applied first.]

**What happened:** [EXPLAIN HERE — describe the successful signing/verification and the forgery failure.]

**Why it matters:** [EXPLAIN HERE — explain that hashing removes the homomorphic structure exploited in Task 8. Discuss PSS padding and how it adds randomness to prevent deterministic attacks. Connect to the EU-CMA security model.]

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
# [INSERT COMMANDS HERE — e.g., python3 task10_weak_hash.py]
```

```python
# [CODE HERE — task10_weak_hash.py]
```

### Output Evidence

> **[INSERT SCREENSHOT HERE — task10_collision.png]**
> Show: both messages, their weak hash values (confirming they match), the signature, and verification passing for the second message.

> **[INSERT SCREENSHOT HERE — task10_sha256_no_collision.png]**
> Show: SHA-256 hashes of the same two messages confirming they differ (no collision).

### Collision Evidence

| Item | Value |
|------|-------|
| Message A | [INSERT] |
| Message B | [INSERT] |
| Weak hash of A | [INSERT] |
| Weak hash of B | [INSERT — must equal A's hash] |
| Signature computed for A | [INSERT — partial] |
| Signature verifies for B? | [INSERT — Yes, demonstrating attack] |
| SHA-256 of A | [INSERT] |
| SHA-256 of B | [INSERT — different from A's] |

### Explanation

**What was done:** [EXPLAIN HERE — describe the weak hash function used and how the collision was found.]

**What happened:** [EXPLAIN HERE — explain that the signature for message A was accepted as valid for message B because they share the same hash.]

**Why it matters:** [EXPLAIN HERE — explain collision resistance as a required property for hash-then-sign security. Discuss why MD5 and SHA-1 are deprecated for signatures, and why SHA-256 or stronger is required. Connect to real-world attacks (e.g., chosen-prefix collisions).]

---

## Task 11 – Comparison and Reflection <a name="task-11"></a>

### Objective

Synthesize all experimental results into a structured comparison table and reflection, clearly articulating the security properties and limitations of each approach explored in this lab.

### Comparison Table

| Scheme | Confidentiality | Integrity | Non-Repudiation | Forgery Resistant | Notes |
|--------|----------------|-----------|-----------------|-------------------|-------|
| Plain RSA (no hash) | | | | | |
| Plain RSA (existential forgery) | | | | | |
| Hash-then-Sign (weak hash) | | | | | |
| Hash-then-Sign (SHA-256, PSS) | | | | | |
| Signature + PKI / CA | | | | | |

> Fill in each cell with: **Yes**, **No**, **Partial**, or **Conditional** — then add a brief note.

---

### Reflection Questions

**1. Why does a digital signature provide non-repudiation when a MAC does not?**

[EXPLAIN HERE]

---

**2. What is the EU-CMA (Existential Unforgeability under Chosen Message Attack) security model, and which scheme in this lab achieves it?**

[EXPLAIN HERE]

---

**3. Why is plain RSA without hashing insecure, even if the private key is never exposed?**

[EXPLAIN HERE]

---

**4. Why must the hash function used in hash-then-sign be collision-resistant?**

[EXPLAIN HERE]

---

**5. What role does public key trust (PKI / certificate authorities) play in making digital signatures useful in practice?**

[EXPLAIN HERE]

---

**6. What is the key takeaway from comparing MAC-based authentication (Lab 5) with digital signatures (this lab)?**

[EXPLAIN HERE]

---

## Conclusion

[WRITE CONCLUSION HERE — summarize the lab's key findings across all 11 tasks. Cover: the role of RSA key pairs in signing/verification, why plain RSA is insecure, how hash-then-sign achieves EU-CMA security, the importance of collision-resistant hash functions, and the necessity of public key infrastructure for real-world deployments.]

---

## Appendix – Python Scripts <a name="appendix"></a>

### A. task1_setup.py

```python
# [CODE HERE]
```

### B. task2_rsa_keygen.py

```python
# [CODE HERE]
```

### C. task3_sign_verify.py

```python
# [CODE HERE]
```

### D. task4_message_tamper.py

```python
# [CODE HERE]
```

### E. task5_sig_tamper.py

```python
# [CODE HERE]
```

### F. task6_pubkey_trust.py

```python
# [CODE HERE]
```

### G. task7_plain_rsa.py

```python
# [CODE HERE]
```

### H. task8_rsa_forgery.py

```python
# [CODE HERE]
```

### I. task9_hash_then_sign.py

```python
# [CODE HERE]
```

### J. task10_weak_hash.py

```python
# [CODE HERE]
```

---

## Pre-Submission Checklist <a name="checklist"></a>

Use this checklist before exporting to PDF.

### Placeholders Cleared

- [ ] Submission date filled in
- [ ] All `[INSERT HASH]` replaced with actual SHA-256 values
- [ ] All `[INSERT]` cells in tables filled in
- [ ] All `[EXPLAIN HERE]` and `[WRITE CONCLUSION HERE]` sections written
- [ ] All `[CODE HERE]` blocks replaced with actual script contents
- [ ] All `[DESCRIBE CHANGE]` rows in tampering tables filled in
- [ ] Comparison table (Task 11) fully filled in with Yes/No/Partial
- [ ] All reflection questions answered

### Screenshots Present

- [ ] task1_directory_setup.png
- [ ] task1_hashes.png
- [ ] task2_keygen_output.png
- [ ] task2_private_pem.png
- [ ] task2_public_pem.png
- [ ] task3_sign_output.png
- [ ] task3_verify_success.png
- [ ] task4_modified_message.png
- [ ] task4_verify_fail.png
- [ ] task5_tampered_sig.png
- [ ] task6_wrong_key_fail.png
- [ ] task6_substitution.png
- [ ] task7_plain_rsa_output.png
- [ ] task8_forgery_output.png
- [ ] task9_sign_output.png
- [ ] task9_forgery_fail.png
- [ ] task10_collision.png
- [ ] task10_sha256_no_collision.png

### Content Check

- [ ] Every task has: Objective + Steps Performed + Commands/Code + Screenshot(s) + Explanation
- [ ] All three sub-questions answered per explanation section (what was done / what happened / why it matters)
- [ ] Task 11 comparison table fully populated
- [ ] Task 11 all six reflection questions answered
- [ ] Appendix contains all 10 scripts
- [ ] No raw output submitted without explanation
- [ ] All code blocks correctly formatted
- [ ] PDF exports cleanly with no broken layout

---

*End of Report*
