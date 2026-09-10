"""Container startup preflight for Syzeteo.

The database schema migration and integrity checks run before the Streamlit
server is started. A failed migration or database check aborts container
startup instead of exposing the application with an unverified schema.
"""

import os

from config import resolve_data_dir, resolve_database_path
from storage import SCHEMA_VERSION, connect


def prepare_database(env=None):
    """Create/migrate and verify the runtime database before the UI starts."""
    runtime_env = os.environ if env is None else env
    data_dir = resolve_data_dir(runtime_env)
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = resolve_database_path(data_dir)

    conn = connect(db_path)
    try:
        schema_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_key_violations = conn.execute("PRAGMA foreign_key_check").fetchall()
    finally:
        conn.close()

    if schema_version != SCHEMA_VERSION:
        raise RuntimeError(
            f"Unsupported SQLite schema version after startup migration: "
            f"{schema_version}; expected {SCHEMA_VERSION}"
        )
    if integrity != "ok":
        raise RuntimeError(f"SQLite integrity_check failed: {integrity}")
    if foreign_key_violations:
        raise RuntimeError(
            f"SQLite foreign_key_check failed: {len(foreign_key_violations)} violation(s)"
        )

    print(
        f"Syzeteo database preflight PASS: schema={schema_version}, "
        f"integrity={integrity}, foreign_keys=ok, path={db_path}",
        flush=True,
    )
    return db_path


def main():
    prepare_database()
    os.execvp(
        "streamlit",
        [
            "streamlit",
            "run",
            "app.py",
            "--server.address=0.0.0.0",
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ],
    )


if __name__ == "__main__":
    main()
