import json
import tempfile
import unittest
from pathlib import Path

from config import resolve_data_dir, resolve_database_path
from storage import (
    CARD_TYPE_CHALLENGE,
    QUESTION_POOL_FORMAT,
    add_learning_unit,
    add_question,
    add_student,
    connect,
    create_course,
    create_round,
    export_question_pool_json,
    game_cards,
    game_roster,
    get_game,
    preview_question_pool_import,
    randomize_teams,
    resolve_instructor_card,
    resolve_question,
    reveal_card,
    start_game,
)


class ReleaseTest(unittest.TestCase):
    def _prepare_game(self, conn):
        create_course(conn, "DEMO")
        cid = conn.execute("SELECT id FROM courses WHERE code='DEMO'").fetchone()[0]
        add_learning_unit(conn, "LE1", "Demo", 1)
        uid = conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]
        qids = []
        for i in range(8):
            add_question(conn, uid, f"Question {i+1}", f"Answer {i+1}")
            qids.append(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        rid = create_round(conn, "Round 1", qids)
        for i in range(8):
            add_student(conn, cid, f"Student {i+1}")
        randomize_teams(conn, cid)
        students = [r["id"] for r in conn.execute("SELECT id FROM students ORDER BY id").fetchall()]
        gid = start_game(conn, rid, cid, students)
        return cid, rid, gid

    def test_rel_01_new_install_uses_syzeteo_database(self):
        with tempfile.TemporaryDirectory() as td:
            path = resolve_database_path(Path(td))
            self.assertEqual(path.name, "syzeteo.sqlite3")
            conn = connect(path)
            conn.close()
            self.assertTrue(path.exists())

    def test_rel_02_syzeteo_data_dir_is_supported(self):
        self.assertEqual(resolve_data_dir({"SYZETEO_DATA_DIR": "/new"}), Path("/new"))
        self.assertEqual(resolve_data_dir({}), Path("persistent"))

    def test_rel_03_non_syzeteo_question_pool_format_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            payload = json.dumps({
                "format": "Other question pool",
                "version": 1,
                "learning_units": [],
                "questions": [],
            }).encode("utf-8")
            with self.assertRaises(ValueError):
                preview_question_pool_import(conn, payload)
            conn.close()

    def test_rel_04_new_exports_use_syzeteo_format(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            payload = json.loads(export_question_pool_json(conn).decode("utf-8"))
            self.assertEqual(payload["format"], QUESTION_POOL_FORMAT)
            self.assertEqual(payload["version"], 1)
            conn.close()

    def test_rel_05_ui_source_contains_no_old_branding(self):
        root = Path(__file__).resolve().parent
        visible_sources = (root / "app.py").read_text(encoding="utf-8") + (root / "auth.py").read_text(encoding="utf-8")
        for term in ("BSDS", "BäM", "MindRounds", "Spielleiter", "Teamjoker"):
            self.assertNotIn(term, visible_sources)

    def test_rel_06_challenge_card_uses_native_value(self):
        self.assertEqual(CARD_TYPE_CHALLENGE, "challenge")
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            _, _, gid = self._prepare_game(conn)
            challenge = [c for c in game_cards(conn, gid) if c["card_type"] == "challenge"]
            self.assertEqual(len(challenge), 1)
            conn.close()

    def test_rel_07_schema_uses_native_team_assist_fields(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            game_cols = {r[1] for r in conn.execute("PRAGMA table_info(games)")}
            card_cols = {r[1] for r in conn.execute("PRAGMA table_info(game_cards)")}
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertIn("team1_assist_used", game_cols)
            self.assertIn("team2_assist_used", game_cols)
            self.assertIn("team_assist_used", card_cols)
            self.assertNotIn("team1_joker_used", game_cols)
            self.assertNotIn("team2_joker_used", game_cols)
            self.assertNotIn("team_joker_used", card_cols)
            conn.close()

    def test_rel_08_team_assist_does_not_block_later_regular_turn(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            _, _, gid = self._prepare_game(conn)
            game = get_game(conn, gid)
            team = int(game["current_team"])
            helper = next(r for r in game_roster(conn, gid, team) if int(r["student_id"]) != int(game["current_student_id"]))
            question = next(c for c in game_cards(conn, gid) if c["card_type"] == "question")
            reveal_card(conn, gid, question["card_no"])
            resolve_question(conn, gid, question["id"], 1, True, helper["student_id"])
            updated_game = get_game(conn, gid)
            flag = updated_game["team1_assist_used"] if team == 1 else updated_game["team2_assist_used"]
            self.assertEqual(flag, 1)
            card = conn.execute("SELECT team_assist_used FROM game_cards WHERE id=?", (question["id"],)).fetchone()
            self.assertEqual(card["team_assist_used"], 1)
            roster = conn.execute(
                "SELECT has_played FROM game_roster WHERE game_id=? AND student_id=?",
                (gid, helper["student_id"]),
            ).fetchone()
            self.assertEqual(roster["has_played"], 0)
            conn.close()

    def test_rel_09_last_card_is_always_instructor_zero_points(self):
        for target_type in ("question", CARD_TYPE_CHALLENGE):
            with self.subTest(target_type=target_type), tempfile.TemporaryDirectory() as td:
                conn = connect(Path(td) / "test.sqlite3")
                _, _, gid = self._prepare_game(conn)
                target = next(c for c in game_cards(conn, gid) if c["card_type"] == target_type)
                conn.execute(
                    "UPDATE game_cards SET revealed=1,resolved=1,points_awarded=0 WHERE game_id=? AND id<>?",
                    (gid, target["id"]),
                )
                conn.commit()
                self.assertTrue(reveal_card(conn, gid, target["card_no"]))
                resolve_instructor_card(conn, gid, target["id"])
                resolved = conn.execute("SELECT resolved,points_awarded FROM game_cards WHERE id=?", (target["id"],)).fetchone()
                game = get_game(conn, gid)
                self.assertEqual((resolved["resolved"], resolved["points_awarded"]), (1, 0))
                self.assertEqual((game["team1_points"], game["team2_points"]), (0, 0))
                self.assertEqual(game["status"], "finished")
                conn.close()

    def test_rel_10_release_tree_contains_no_persistent_database(self):
        root = Path(__file__).resolve().parent
        forbidden = []
        for pattern in ("*.sqlite", "*.sqlite3", "*.sqlite3-*", "*.backup", "*.bak"):
            forbidden.extend(root.rglob(pattern))
        self.assertEqual(forbidden, [])

    def test_rel_11_sql_schema_contains_no_old_branding_terms(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            schema = "\n".join(r[0] or "" for r in conn.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL"))
            for term in ("baem", "joker", "bsds", "mindrounds"):
                self.assertNotIn(term, schema.lower())
            conn.close()

    def test_rel_12_runtime_python_contains_no_old_technical_names(self):
        root = Path(__file__).resolve().parent
        runtime = "\n".join((root / name).read_text(encoding="utf-8") for name in ("app.py", "auth.py", "config.py", "storage.py"))
        for term in ("baem_joker", "team_joker_used", "team1_joker_used", "team2_joker_used", "BSDS_DATA_DIR", "bsds.sqlite3", "MINDROUNDS_DATA_DIR", "mindrounds.sqlite3"):
            self.assertNotIn(term, runtime)

    def test_rel_13_schema_v2_preserves_data_from_older_internal_schema(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test.sqlite3"
            import sqlite3
            legacy = sqlite3.connect(path)
            legacy.execute("CREATE TABLE courses (id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, title TEXT NOT NULL DEFAULT '', active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL)")
            legacy.execute("INSERT INTO courses VALUES(1,'KEEP','Existing course',1,'2026-08-27T00:00:00+00:00')")
            legacy.execute("PRAGMA user_version=1")
            legacy.commit()
            legacy.close()

            conn = connect(path)
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertEqual(conn.execute("SELECT code FROM courses WHERE id=1").fetchone()[0], "KEEP")
            settings_table = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='app_settings'").fetchone()
            self.assertIsNotNone(settings_table)
            conn.close()


if __name__ == "__main__":
    unittest.main()
