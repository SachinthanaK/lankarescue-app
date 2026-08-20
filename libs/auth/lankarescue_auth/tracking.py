"""Opaque tracking-token generation and verification."""

import hashlib
import hmac
import secrets


def generate_tracking_token() -> str:
    """Return a high-entropy token suitable for giving to an anonymous citizen."""
    return secrets.token_urlsafe(32)


def hash_tracking_token(token: str) -> str:
    """Hash a token before storage; the plaintext token is never persisted."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_tracking_token(token: str, expected_hash: str) -> bool:
    """Compare token hashes without leaking timing information."""
    return hmac.compare_digest(hash_tracking_token(token), expected_hash)
