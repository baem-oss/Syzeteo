import tempfile
import unittest
from pathlib import Path

from storage import connect, create_course, question_analysis_rows


class QuestionAnalysisTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")
        create_course(self.conn, "A")
        create_course(self.conn, "B")
        self.course_a = self.conn.execute("SELECT id FROM courses WHERE code='A'").fetchone()[0]
        self.course_b = self.conn.execute("SELECT id FROM courses WHERE code='B'").fetchone()[0]
        self.conn.execute("INSERT INTO rounds(name,created_at) VALUES('R1','2026-09-01T00:00:00+00:00')")
        self.conn.execute("INSERT INTO rounds(name,created_at) VALUES('R2','2026-09-02T00:00:00+00:00')")
        self.round1 = self.conn.execute("SELECT id FROM rounds WHERE name='R1'").fetchone()[0]
        self.round2 = self.conn.execute("SELECT id FROM rounds WHERE name='R2'").fetchone()[0]
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def _game(self, round_id, course_id, status="finished", suffix="1"):
        finished = f"2026-09-0{suffix}T10:10:00+00:00" if status == "finished" else None
        cur = self.conn.execute(
            "INSERT INTO games(round_id,course_id,status,started_at,finished_at) VALUES(?,?,?,?,?)",
            (round_id, course_id, status, f"2026-09-0{suffix}T10:00:00+00:00", finished),
        )
        return cur.lastrowid

    def _card(self, game_id, card_no, qid, text, points, resolved_at, card_type="question", assist=0):
        self.conn.execute(
            """
            INSERT INTO game_cards(
                game_id,card_no,card_type,question_id,question_text_snapshot,unit_code_snapshot,
                revealed,resolved,resolved_at,team_assist_used,points_awarded
            ) VALUES(?,?,?,?,?,?,1,1,?,?,?)
            """,
            (game_id, card_no, card_type, qid, text, "LE10", resolved_at, assist, points),
        )
        self.conn.commit()

    def test_analysis_counts_correct_and_incorrect_regular_questions(self):
        gid = self._game(self.round1, self.course_a)
        self._card(gid, 1, 11, "Question A", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid, 2, 12, "Question B", 0, "2026-09-01T10:02:00+00:00")
        self._card(gid, 3, 13, "Instructor final", 0, "2026-09-01T10:09:00+00:00")
        rows = question_analysis_rows(self.conn)
        by_qid = {r["question_id"]: r for r in rows}
        self.assertEqual((by_qid[11]["attempts"], by_qid[11]["correct"], by_qid[11]["wrong"], by_qid[11]["success_rate"]), (1, 1, 0, 100.0))
        self.assertEqual((by_qid[12]["attempts"], by_qid[12]["correct"], by_qid[12]["wrong"], by_qid[12]["success_rate"]), (1, 0, 1, 0.0))

    def test_analysis_excludes_final_instructor_card_and_challenge_card(self):
        gid = self._game(self.round1, self.course_a)
        self._card(gid, 1, 11, "Regular", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid, 2, None, None, 2, "2026-09-01T10:02:00+00:00", card_type="challenge")
        self._card(gid, 3, 13, "Instructor final", 0, "2026-09-01T10:09:00+00:00")
        rows = question_analysis_rows(self.conn)
        self.assertEqual([(r["question_id"], r["attempts"]) for r in rows], [(11, 1)])

    def test_analysis_excludes_running_and_aborted_games(self):
        gid_a = self._game(self.round1, self.course_a, "aborted")
        self._card(gid_a, 1, 11, "Aborted question", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid_a, 2, 12, "Later", 0, "2026-09-01T10:02:00+00:00")
        gid_b = self._game(self.round1, self.course_b, "running")
        self._card(gid_b, 1, 11, "Running question", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid_b, 2, 12, "Later", 0, "2026-09-01T10:02:00+00:00")
        self.assertEqual(question_analysis_rows(self.conn), [])

    def test_analysis_can_be_scoped_to_one_course_or_all_courses(self):
        gid_a = self._game(self.round1, self.course_a, suffix="1")
        self._card(gid_a, 1, 11, "Same question", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid_a, 2, 90, "Final A", 0, "2026-09-01T10:09:00+00:00")
        gid_b = self._game(self.round1, self.course_b, suffix="2")
        self._card(gid_b, 1, 11, "Same question", 0, "2026-09-02T10:01:00+00:00")
        self._card(gid_b, 2, 91, "Final B", 0, "2026-09-02T10:09:00+00:00")
        all_rows = question_analysis_rows(self.conn)
        self.assertEqual((all_rows[0]["attempts"], all_rows[0]["correct"], all_rows[0]["wrong"], all_rows[0]["success_rate"]), (2, 1, 1, 50.0))
        a_rows = question_analysis_rows(self.conn, self.course_a)
        self.assertEqual((a_rows[0]["attempts"], a_rows[0]["correct"], a_rows[0]["wrong"], a_rows[0]["success_rate"]), (1, 1, 0, 100.0))

    def test_analysis_separates_changed_question_versions(self):
        gid_a = self._game(self.round1, self.course_a, suffix="1")
        self._card(gid_a, 1, 11, "Old wording", 1, "2026-09-01T10:01:00+00:00")
        self._card(gid_a, 2, 90, "Final A", 0, "2026-09-01T10:09:00+00:00")
        gid_b = self._game(self.round1, self.course_b, suffix="2")
        self._card(gid_b, 1, 11, "New wording", 0, "2026-09-02T10:01:00+00:00")
        self._card(gid_b, 2, 91, "Final B", 0, "2026-09-02T10:09:00+00:00")
        rows = question_analysis_rows(self.conn)
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["question_text"] for r in rows}, {"Old wording", "New wording"})

    def test_analysis_contains_no_individual_student_fields_and_counts_team_assist_normally(self):
        gid = self._game(self.round1, self.course_a)
        self._card(gid, 1, 11, "Assisted", 1, "2026-09-01T10:01:00+00:00", assist=1)
        self._card(gid, 2, 90, "Final", 0, "2026-09-01T10:09:00+00:00")
        row = question_analysis_rows(self.conn)[0]
        self.assertEqual(row["attempts"], 1)
        self.assertEqual(row["correct"], 1)
        self.assertFalse(any("student" in key or "player" in key for key in row.keys()))


if __name__ == "__main__":
    unittest.main()
