import tempfile
import unittest
from pathlib import Path

from storage import (
    TIC_TAC_TOE_LINES,
    add_learning_unit,
    add_question,
    add_student,
    connect,
    create_course,
    create_round,
    game_cards,
    get_game,
    randomize_teams,
    resolve_question,
    reveal_card,
    start_game,
    tic_tac_toe_line,
    undo_last_action,
)


def board(*moves):
    """Nine cards in card_no order; moves are (position, scoring team or None) in scoring order."""
    cards = [{"points_team": None, "resolved_at": None} for _ in range(9)]
    for step, (pos, team) in enumerate(moves, start=1):
        cards[pos] = {"points_team": team, "resolved_at": f"2026-10-28T10:{step:02d}:00+00:00"}
    return cards


class TicTacToeTest(unittest.TestCase):
    def test_no_line_without_three_scored_cards_of_one_team(self):
        self.assertIsNone(tic_tac_toe_line(board()))
        self.assertIsNone(tic_tac_toe_line(board((0, 1), (1, 2), (2, 1))))
        self.assertIsNone(tic_tac_toe_line(board((0, 1), (1, None), (2, 1))))

    def test_every_line_is_detected_with_its_direction(self):
        for line, direction in TIC_TAC_TOE_LINES.items():
            with self.subTest(line=line):
                self.assertEqual(tic_tac_toe_line(board(*[(pos, 2) for pos in line])), (2, line, direction))

    def test_first_completed_line_wins(self):
        cards = board((6, 1), (0, 2), (7, 1), (1, 2), (2, 2), (8, 1))
        self.assertEqual(tic_tac_toe_line(cards), (2, (0, 1, 2), "row"))

    def test_scored_game_cards_form_line_and_undo_removes_it(self):
        with tempfile.TemporaryDirectory() as td:
            conn = connect(Path(td) / "test.sqlite3")
            create_course(conn, "TTT")
            cid = conn.execute("SELECT id FROM courses WHERE code='TTT'").fetchone()[0]
            add_learning_unit(conn, "LE1", "Test", 1)
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
            starter = get_game(conn, gid)["current_team"]
            for pos, points in ((0, 1), (3, 0), (1, 1), (4, 1), (2, 1)):
                card = game_cards(conn, gid)[pos]
                reveal_card(conn, gid, card["card_no"])
                resolve_question(conn, gid, card["id"], points)
            self.assertEqual(tic_tac_toe_line(game_cards(conn, gid)), (starter, (0, 1, 2), "row"))
            undo_last_action(conn, gid)
            self.assertIsNone(tic_tac_toe_line(game_cards(conn, gid)))
            conn.close()

    def test_card_markers_have_matching_css(self):
        source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
        self.assertIn("key=f\"syzeteo_card_{state}_{marker}{card['id']}\"", source)
        for marker in ("done_t1_", "done_t2_", *(f"_line_{d}_" for d in set(TIC_TAC_TOE_LINES.values()))):
            self.assertIn(marker, source)


if __name__ == "__main__":
    unittest.main()
