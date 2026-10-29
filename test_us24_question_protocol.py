"""US #24 acceptance tests for the existing question protocol contract.

Tests document current, unambiguous behavior. Pending domain decisions
(revealed-only, aborted games, final instructor card) remain explicit in docs.
"""
import tempfile
import unittest
from pathlib import Path

from storage import connect, create_course, protocol_rows


class US24QuestionProtocolAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "acceptance.sqlite3")
        for code in ("A", "B"):
            create_course(self.conn, code)
        self.courses = {
            r["code"]: r["id"]
            for r in self.conn.execute("SELECT id,code FROM courses")
        }
        for name in ("R1", "R2"):
            self.conn.execute(
                "INSERT INTO rounds(name,created_at) VALUES(?,?)",
                (name, "2026-10-01T00:00:00+00:00"),
            )
        self.rounds = {
            r["name"]: r["id"]
            for r in self.conn.execute("SELECT id,name FROM rounds")
        }
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def game(self, course="A", rnd="R1", status="running"):
        cursor = self.conn.execute(
            "INSERT INTO games(round_id,course_id,status,started_at) VALUES(?,?,?,?)",
            (self.rounds[rnd], self.courses[course], status,
             "2026-10-01T10:00:00+00:00"),
        )
        self.conn.commit()
        return cursor.lastrowid

    def card(self, game, position, question_id, text, *,
             card_type="question", revealed=1, resolved=1):
        self.conn.execute(
            """INSERT INTO game_cards(
                 game_id,card_no,card_type,question_id,question_text_snapshot,
                 unit_code_snapshot,revealed,resolved,resolved_at)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (game, position, card_type, question_id, text, "LE1",
             revealed, resolved,
             "2026-10-01T10:05:00+00:00" if resolved else None),
        )
        self.conn.commit()

    def test_us24_resolved_questions_have_course_round_and_position(self):
        game_a = self.game("A", "R1")
        game_b = self.game("B", "R2")
        self.card(game_a, 1, 101, "Frage A")
        self.card(game_b, 4, 202, "Frage B")
        rows = protocol_rows(self.conn)
        actual = {(r["course_code"], r["round_name"], r["position"],
                   r["question_id"], r["question_text"]) for r in rows}
        self.assertEqual(actual, {
            ("A", "R1", 1, 101, "Frage A"),
            ("B", "R2", 4, 202, "Frage B"),
        })

    def test_us24_unresolved_and_challenge_cards_not_in_question_protocol(self):
        gid = self.game()
        self.card(gid, 1, 101, "Gewertet")
        self.card(gid, 2, 102, "Nur aufgedeckt", resolved=0)
        self.card(gid, 3, None, None, card_type="challenge")
        self.assertEqual(
            [(row["question_id"], row["question_text"]) for row in protocol_rows(self.conn)],
            [(101, "Gewertet")],
        )

    def test_us24_question_snapshot_is_independent_of_pool_changes(self):
        gid = self.game()
        self.card(gid, 1, 101, "Ursprünglicher Fragetext")
        self.conn.execute("INSERT INTO learning_units(code,title,position) VALUES('LE1','Unit',1)")
        self.conn.execute(
            """INSERT INTO questions(id,learning_unit_id,question_text,answer_text,created_at,updated_at)
               VALUES(101,(SELECT id FROM learning_units WHERE code='LE1'),
                      'Geänderter Fragetext','Antwort','2026-10-01','2026-10-01')"""
        )
        self.conn.commit()
        self.assertEqual(
            self.conn.execute("SELECT question_text FROM questions WHERE id=101").fetchone()[0],
            "Geänderter Fragetext",
        )
        self.assertEqual(protocol_rows(self.conn)[0]["question_text"],
                         "Ursprünglicher Fragetext")
        self.assertEqual(protocol_rows(self.conn)[0]["unit_code"], "LE1")
        
    def test_us24_protocol_has_status_and_resolution_timestamp(self):
        gid = self.game(status="aborted")
        self.card(gid, 1, 101, "Bereits bearbeitet")
        row = protocol_rows(self.conn)[0]
        self.assertEqual(row["status"], "aborted")
        self.assertEqual(row["resolved_at"], "2026-10-01T10:05:00+00:00")
        self.assertEqual(row["course_code"], "A")


    def test_us24_aborted_game_keeps_resolved_questions_until_deleted(self):
        from storage import abort_game, delete_aborted_game
        gid = self.game()
        self.card(gid, 1, 301, "Abgeschlossene Frage")
        self.card(gid, 2, 302, "Nur aufgedeckt", resolved=0)
        abort_game(self.conn, gid)
        rows = protocol_rows(self.conn)
        self.assertEqual([(r["question_id"], r["status"]) for r in rows],
                         [(301, "aborted")])
        delete_aborted_game(self.conn, gid)
        self.assertEqual(protocol_rows(self.conn), [])


if __name__ == "__main__":
    unittest.main()
