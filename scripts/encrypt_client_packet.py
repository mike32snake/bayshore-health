#!/usr/bin/env python3
"""Encrypt a client proposal into clients/<slug>/payload.json for the password gate.

Usage: python3 scripts/encrypt_client_packet.py <slug> <password> <plaintext.html>

Matches the WebCrypto decrypt in clients/<slug>/index.html:
PBKDF2-SHA256 (200,000 iterations) -> AES-256-GCM, ciphertext||tag, base64 fields.
Run scripts/verify_client_packet.py afterwards.
"""
import base64, json, os, sys
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 200_000

def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__); return 2
    slug, pw, src = sys.argv[1], sys.argv[2].encode(), Path(sys.argv[3])
    out = Path(__file__).resolve().parent.parent / "clients" / slug / "payload.json"
    plain = src.read_bytes()
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw)
    ct = AESGCM(key).encrypt(iv, plain, None)
    out.write_text(json.dumps({"salt": base64.b64encode(salt).decode(), "iterations": ITER,
                               "iv": base64.b64encode(iv).decode(), "ciphertext": base64.b64encode(ct).decode()}))
    print(f"wrote {out} ({out.stat().st_size} bytes; plaintext {len(plain)} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
