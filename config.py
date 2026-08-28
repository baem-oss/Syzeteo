import os
from pathlib import Path

DEFAULT_DATA_DIR = Path("./persistent")
DEFAULT_DB_NAME = "syzeteo.sqlite3"


def resolve_data_dir(env=None):
    env = os.environ if env is None else env
    value = env.get("SYZETEO_DATA_DIR")
    return Path(value) if value else DEFAULT_DATA_DIR


def resolve_database_path(data_dir: Path):
    return Path(data_dir) / DEFAULT_DB_NAME
