
# 🧠 **Shortened Instructions (FULL POINT CHECKLIST)**

Use this as your **report outline** 👇

---

## 🔹 Task 1 – Setup + Messages

* Create folder + 3 message files
* Show:

  * `pwd`, `ls`, `cat`
  * SHA-256 hashes
* Explain:

  * Purpose of hashing

---

## 🔹 Task 2 – Key Generation

* Generate:

  * private key (2048-bit)
  * public key
* Show files + optional inspection
* Explain:

  * Private key = signing
  * Public key = verification

---

## 🔹 Task 3 – Sign + Verify

* Sign `msg1.txt`
* Verify signature
* Show:

  * successful verification output
* Explain:

  * Signature proves integrity + authenticity

---

## 🔹 Task 4 – Message Tampering

* Modify message
* Verify with original signature → FAIL
* Explain:

  * Signature tied to exact message

---

## 🔹 Task 5 – Signature Tampering

* Modify signature (1 byte)
* Verify → FAIL
* Explain:

  * Signature integrity protection

---

## 🔹 Task 6 – Public Key Trust

* Generate fake key pair
* Show:

  * Original signature fails with wrong key
  * Fake signature works with fake key
* Explain:

  * Public key must be authentic

---

## 🔹 Task 7 – Raw RSA Demo (Python)

* Run toy RSA signing
* Show:

  * signature + verification works
* Explain:

  * Math works ≠ secure

---

## 🔹 Task 8 – RSA Forgery

* Show:

  * s1 * s2 → valid signature for m1 * m2
* Explain:

  * Multiplicative property = vulnerability
  * Breaks unforgeability

---

## 🔹 Task 9 – Hash-then-Sign

* Hash message → sign hash
* Show:

  * verification success
  * change message → fails
* Explain:

  * Hash binds structure + supports long messages

---

## 🔹 Task 10 – Weak Hash Collision

* Create weak hash
* Find collision (two messages same hash)
* Explain:

  * Same hash → signature reuse → insecure
  * Need collision resistance

---

## 🔹 Task 11 – Comparison + Reflection

### Table:

| Method         | Works? | Secure? | Key Issue            |
| -------------- | ------ | ------- | -------------------- |
| OpenSSL RSA    | Yes    | Yes     | Requires trusted key |
| Raw RSA        | Yes    | No      | Multiplicative       |
| Forgery RSA    | Yes    | No      | Signature reuse      |
| Hash-then-sign | Yes    | Yes     | Depends on hash      |
| Weak hash      | Yes    | No      | Collisions           |

### Reflection (1 paragraph):

Answer:

* What signatures provide
* Why raw RSA fails
* Why hashing helps
* Why public key trust matters
* What you learned

---

# ⚡ Pro Tips (Easy Points People Miss)

* ALWAYS include screenshots (huge grading weight) 
* Don’t just show output → **explain it**
* Clearly label each task section
* Mention:

  * integrity
  * authentication
  * non-repudiation

---

