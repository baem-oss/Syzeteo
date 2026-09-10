import sqlite3
import tempfile
import unittest
from pathlib import Path

from startup import prepare_database


class StartupMigrationTest(unittest.TestCase):
    def _make_schema_v2_database(self, path: Path):
        conn = sqlite3.connect(path)
        conn.executescript(
            """
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL DEFAULT '',
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            CREATE TABLE rounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                locked INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                locked_at TEXT
            );
            CREATE TABLE games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                round_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'running',
                started_at TEXT NOT NULL,
                finished_at TEXT,
                team1_points INTEGER NOT NULL DEFAULT 0,
                team2_points INTEGER NOT NULL DEFAULT 0,
                team1_assist_used INTEGER NOT NULL DEFAULT 0,
                team2_assist_used INTEGER NOT NULL DEFAULT 0,
                current_student_id INTEGER,
                current_team INTEGER,
                turn_no INTEGER NOT NULL DEFAULT 1,
                player_selection_mode TEXT NOT NULL DEFAULT 'manual',
                UNIQUE(round_id, course_id)
            );
            CREATE TABLE app_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            );
            INSERT INTO courses(id,code,title,active,created_at)
                VALUES(1,'KEEP','Existing',1,'2026-09-01T00:00:00+00:00');
            INSERT INTO rounds(id,name,locked,created_at)
                VALUES(1,'Round 1',1,'2026-09-01T00:00:00+00:00');
            INSERT INTO games(id,round_id,course_id,status,started_at,finished_at,team1_points,team2_points)
                VALUES(1,1,1,'finished','2026-09-01T10:00:00+00:00','2026-09-01T11:00:00+00:00',4,3);
            PRAGMA user_version=2;
            """
        )
        conn.commit()
        conn.close()

    def test_startup_preflight_migrates_schema_v2_before_ui_start(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "syzeteo.sqlite3"
            self._make_schema_v2_database(path)

            returned = prepare_database({"SYZETEO_DATA_DIR": td})

            self.assertEqual(returned, path)
            conn = sqlite3.connect(path)
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 3)
            self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(conn.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(
                conn.execute("SELECT team1_name,team2_name FROM courses WHERE id=1").fetchone(),
                ("Team 1", "Team 2"),
            )
            self.assertEqual(
                conn.execute("SELECT team1_name_snapshot,team2_name_snapshot FROM games WHERE id=1").fetchone(),
                ("Team 1", "Team 2"),
            )
            conn.close()

    def test_docker_starts_preflight_instead_of_streamlit_directly(self):
        dockerfile = (Path(__file__).resolve().parent / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn('CMD ["python", "startup.py"]', dockerfile)
        self.assertNotIn('CMD ["streamlit", "run", "app.py"', dockerfile)

    def test_startup_preflight_rejects_unsupported_future_schema(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "syzeteo.sqlite3"
            conn = sqlite3.connect(path)
            conn.execute("PRAGMA user_version=99")
            conn.commit()
            conn.close()

            with self.assertRaisesRegex(RuntimeError, "Unsupported SQLite schema version"):
                prepare_database({"SYZETEO_DATA_DIR": td})

    def test_startup_preflight_rejects_foreign_key_violations(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "syzeteo.sqlite3"
            conn = sqlite3.connect(path)
            conn.executescript(
                """
                PRAGMA foreign_keys=OFF;
                CREATE TABLE courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL DEFAULT '',
                    team1_name TEXT NOT NULL DEFAULT 'Team 1',
                    team2_name TEXT NOT NULL DEFAULT 'Team 2',
                    active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                    first_name TEXT NOT NULL DEFAULT '',
                    last_name TEXT NOT NULL DEFAULT '',
                    display_name TEXT NOT NULL,
                    team INTEGER CHECK(team IN (1,2) OR team IS NULL),
                    active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    UNIQUE(course_id, display_name)
                );
                INSERT INTO students(id,course_id,display_name,created_at)
                    VALUES(1,999,'Orphan','2026-09-10T00:00:00+00:00');
                PRAGMA user_version=3;
                """
            )
            conn.commit()
            conn.close()

            with self.assertRaisesRegex(RuntimeError, "foreign_key_check failed"):
                prepare_database({"SYZETEO_DATA_DIR": td})


if __name__ == "__main__":
    unittest.main()
