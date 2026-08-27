#!/usr/bin/env python3
"""Verify a password-gated client packet under clients/<slug>/.

Usage: python3 scripts/verify_client_packet.py <slug> <password> [expected-phrase ...]

Checks:
  1. clients/<slug>/index.html and payload.json exist.
  2. The gate is noindex and points at payload.json.
  3. payload.json decrypts with the password (same PBKDF2/AES-GCM as the gate JS).
  4. A wrong password is rejected.
  5. The decrypted HTML contains every expected phrase.
  6. Neither the gate nor the decrypted HTML contains an em-dash or en-dash.
Exit code 0 = all checks pass.
"""
import base64, json, sys
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive(pw: bytes, salt: bytes, iters: int) -> bytes:
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters).derive(pw)

def decrypt(payload: dict, pw: str) -> bytes:
    key = derive(pw.encode(), base64.b64decode(payload["salt"]), payload["iterations"])
    return AESGCM(key).decrypt(base64.b64decode(payload["iv"]), base64.b64decode(payload["ciphertext"]), None)

def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__); return 2
    slug, pw, phrases = sys.argv[1], sys.argv[2], sys.argv[3:]
    root = Path(__file__).resolve().parent.parent / "clients" / slug
    gate, payload_path = root / "index.html", root / "payload.json"
    fails = []
    def check(ok, msg):
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok: fails.append(msg)

    check(gate.exists(), f"{gate} exists")
    check(payload_path.exists(), f"{payload_path} exists")
    if fails: return 1
    g = gate.read_text()
    check('name="robots" content="noindex' in g, "gate is noindex")
    check("payload.json" in g, "gate fetches payload.json")
    payload = json.loads(payload_path.read_text())
    try:
        html = decrypt(payload, pw).decode()
        check(True, "payload decrypts with the password")
    except Exception as e:
        check(False, f"payload decrypts with the password ({e})"); return 1
    try:
        decrypt(payload, pw + "x"); check(False, "wrong password is rejected")
    except Exception:
        check(True, "wrong password is rejected")
    for p in phrases:
        check(p in html, f"decrypted HTML contains {p!r}")
    for name, text in (("gate", g), ("proposal", html)):
        check("—" not in text and "–" not in text, f"{name} has no em/en dashes")
    print(f"\n{len(fails)} failure(s)")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
