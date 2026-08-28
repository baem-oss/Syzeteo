import hashlib
import hmac
import os
import sqlite3
import unicodedata
from datetime import datetime, timezone

PBKDF2_ITERATIONS = 310_000
MIN_PASSWORD_LENGTH = 12


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def normalize_username(value: str) -> str:
    return unicodedata.normalize("NFKC", (value or "")).strip()


def username_key(value: str) -> str:
    return normalize_username(value).casefold()


def hash_password(password: str, *, salt: bytes | None = None, iterations: int = PBKDF2_ITERATIONS):
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return salt.hex(), digest.hex(), iterations


def verify_password(password: str, salt_hex: str, digest_hex: str, iterations: int) -> bool:
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", (password or "").encode("utf-8"), salt, int(iterations))
    return hmac.compare_digest(actual, expected)


def ensure_user_table(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username_key TEXT PRIMARY KEY,
            username_display TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            password_iterations INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            last_login_at TEXT
        )
        """
    )
    conn.commit()


def user_count(conn: sqlite3.Connection) -> int:
    ensure_user_table(conn)
    return int(conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])


def create_admin(conn: sqlite3.Connection, username: str, password: str, confirmation: str):
    ensure_user_table(conn)
    username = normalize_username(username)
    if user_count(conn) > 0:
        return False, "auth.error.account_exists"
    if len(username) < 2:
        return False, "auth.error.username_too_short"
    if len(password or "") < MIN_PASSWORD_LENGTH:
        return False, "auth.error.password_too_short"
    if password != confirmation:
        return False, "auth.error.password_mismatch"
    salt, digest, iterations = hash_password(password)
    conn.execute(
        "INSERT INTO users VALUES(?,?,?,?,?,?,?)",
        (username_key(username), username, salt, digest, iterations, now_iso(), now_iso()),
    )
    conn.commit()
    return True, "auth.success.account_created"


def authenticate(conn: sqlite3.Connection, username: str, password: str):
    ensure_user_table(conn)
    row = conn.execute(
        "SELECT * FROM users WHERE username_key=?", (username_key(username),)
    ).fetchone()
    if row is None or not verify_password(password, row["password_salt"], row["password_hash"], row["password_iterations"]):
        return False, "auth.error.invalid_credentials", None
    conn.execute("UPDATE users SET last_login_at=? WHERE username_key=?", (now_iso(), row["username_key"]))
    conn.commit()
    return True, "auth.ok", row["username_display"]


def change_password(conn: sqlite3.Connection, username: str, old_password: str, new_password: str, confirmation: str):
    ok, _, display = authenticate(conn, username, old_password)
    if not ok:
        return False, "auth.error.old_password_wrong"
    if len(new_password or "") < MIN_PASSWORD_LENGTH:
        return False, "auth.error.new_password_too_short"
    if new_password != confirmation:
        return False, "auth.error.new_password_mismatch"
    salt, digest, iterations = hash_password(new_password)
    conn.execute(
        "UPDATE users SET password_salt=?,password_hash=?,password_iterations=? WHERE username_key=?",
        (salt, digest, iterations, username_key(display)),
    )
    conn.commit()
    return True, "auth.success.password_changed"


def change_username(conn: sqlite3.Connection, old_username: str, password: str, new_username: str):
    ok, _, display = authenticate(conn, old_username, password)
    if not ok:
        return False, "auth.error.password_wrong", None
    new_username = normalize_username(new_username)
    if len(new_username) < 2:
        return False, "auth.error.new_username_too_short", None
    new_key = username_key(new_username)
    existing = conn.execute("SELECT 1 FROM users WHERE username_key=? AND username_key<>?", (new_key, username_key(display))).fetchone()
    if existing:
        return False, "auth.error.username_taken", None
    conn.execute(
        "UPDATE users SET username_key=?,username_display=? WHERE username_key=?",
        (new_key,new_username,username_key(display)),
    )
    conn.commit()
    return True, "auth.success.username_changed", new_username
