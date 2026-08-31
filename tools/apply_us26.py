from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def insert_before_once(text: str, anchor: str, insertion: str, marker: str, label: str) -> str:
    if marker in text:
        return text
    count = text.count(anchor)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(anchor, insertion + anchor, 1)


def patch_storage() -> None:
    path = ROOT / "storage.py"
    text = path.read_text(encoding="utf-8")
    marker = "def abort_game(conn, game_id):"
    if marker not in text:
        anchor = "\n\ndef game_cards(conn, game_id):\n"
        insertion = r'''


def abort_game(conn, game_id):
    """Abort an ongoing game without treating it as regularly completed."""
    gid = int(game_id)
    game = conn.execute("SELECT id,status FROM games WHERE id=?", (gid,)).fetchone()
    if not game:
        raise StorageError("error.game.abort_not_found")
    if game["status"] != "running":
        raise StorageError("error.game.abort_running_only")
    try:
        conn.execute("BEGIN")
        updated = conn.execute(
            "UPDATE games SET status='aborted' WHERE id=? AND status='running'",
            (gid,),
        )
        if updated.rowcount != 1:
            raise StorageError("error.game.abort_running_only")
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def delete_aborted_game(conn, game_id):
    """Delete an aborted game and all data that belongs exclusively to it."""
    gid = int(game_id)
    game = conn.execute("SELECT id,status FROM games WHERE id=?", (gid,)).fetchone()
    if not game:
        raise StorageError("error.game.delete_not_found")
    if game["status"] != "aborted":
        raise StorageError("error.game.delete_aborted_only")
    try:
        conn.execute("BEGIN")
        deleted = conn.execute(
            "DELETE FROM games WHERE id=? AND status='aborted'",
            (gid,),
        )
        if deleted.rowcount != 1:
            raise StorageError("error.game.delete_aborted_only")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
'''
        text = insert_before_once(text, anchor, insertion, marker, "storage game lifecycle")
    path.write_text(text, encoding="utf-8")


def patch_app() -> None:
    path = ROOT / "app.py"
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '    create_course, create_round, delete_course, delete_learning_unit, delete_question,\n',
        '    abort_game, create_course, create_round, delete_aborted_game, delete_course, delete_learning_unit, delete_question,\n',
        "app storage imports",
    )
    text = replace_once(text, 'APP_VERSION = "1.0.0"', 'APP_VERSION = "1.1.0-dev1"', "app version")

    text = replace_once(
        text,
        '        "running": tr("question_log.coverage.running"),\n    }.get(state, state)\n',
        '        "running": tr("question_log.coverage.running"),\n        "aborted": tr("question_log.coverage.aborted"),\n    }.get(state, state)\n',
        "coverage state label",
    )

    text = replace_once(
        text,
        '            status_labels={"finished":tr("status.finished"),"running":tr("status.running")}\n',
        '            status_labels={"finished":tr("status.finished"),"running":tr("status.running"),"aborted":tr("status.aborted")}\n',
        "dashboard history status labels",
    )

    text = replace_once(
        text,
        '                col_status:{"finished":tr("status.finished"),"running":tr("status.running")}.get(row["status"],row["status"]), col_played:((row["resolved_at"] or row["started_at"] or "")[:10]),\n',
        '                col_status:{"finished":tr("status.finished"),"running":tr("status.running"),"aborted":tr("status.aborted")}.get(row["status"],row["status"]), col_played:((row["resolved_at"] or row["started_at"] or "")[:10]),\n',
        "question log status labels",
    )

    text = replace_once(
        text,
        '                elif game and game["status"]=="running":\n                    status=tr("question_log.coverage.running"); finished_all=False\n                else:\n                    status=tr("question_log.coverage.open"); finished_all=False\n',
        '                elif game and game["status"]=="running":\n                    status=tr("question_log.coverage.running"); finished_all=False\n                elif game and game["status"]=="aborted":\n                    status=tr("question_log.coverage.aborted"); finished_all=False\n                else:\n                    status=tr("question_log.coverage.open"); finished_all=False\n',
        "question log aborted coverage",
    )

    abort_marker = 'game.abort.button'
    if abort_marker not in text:
        anchor = '        st.caption(tr("game.player_mode.running", mode=regular_mode_label))\n\n'
        insertion = '''        abort_confirm_key=f"abort_confirm_{gid}"\n        if st.button(tr("game.abort.button"),key=f"abort_game_{gid}",type="secondary"):\n            st.session_state[abort_confirm_key]=True\n            rerun()\n        if st.session_state.get(abort_confirm_key):\n            st.warning(tr("game.abort.warning",round_name=game["round_name"],course_code=game["course_code"]))\n            abort_yes,abort_no=st.columns(2)\n            if abort_yes.button(tr("game.abort.confirm"),key=f"abort_game_confirm_{gid}",type="primary"):\n                try:\n                    aborted_round=game["round_name"]\n                    aborted_course=game["course_code"]\n                    abort_game(conn,gid)\n                    clear_game_ui_state(gid)\n                    st.session_state.pop("active_game",None)\n                    st.session_state.pop(abort_confirm_key,None)\n                    st.session_state["game_abort_success"]={"round_name":aborted_round,"course_code":aborted_course}\n                    st.session_state.page_nav=PAGE_INSTRUCTOR_SETTINGS\n                    rerun()\n                except Exception as e:\n                    show_error(e)\n            if abort_no.button(tr("game.abort.cancel"),key=f"abort_game_cancel_{gid}"):\n                st.session_state.pop(abort_confirm_key,None)\n                rerun()\n\n'''
        text = insert_before_once(text, anchor, insertion, abort_marker, "game abort UI")

    success_render_marker = 'tr("game.abort.success"'
    if success_render_marker not in text:
        anchor = '    st.caption(tr("settings.caption"))\n\n'
        insertion = '''    aborted_flash=st.session_state.pop("game_abort_success",None)\n    if aborted_flash:\n        st.success(tr("game.abort.success",**aborted_flash))\n    deleted_flash=st.session_state.pop("game_delete_success",None)\n    if deleted_flash:\n        st.success(tr("settings.aborted.deleted",**deleted_flash))\n\n'''
        text = insert_before_once(text, anchor, insertion, success_render_marker, "instructor flash messages")

    aborted_settings_marker = 'settings.aborted.title'
    if aborted_settings_marker not in text:
        anchor = '\nelif PAGE==PAGE_ACCOUNT:\n'
        insertion = '''\n    st.divider()\n    st.subheader(tr("settings.aborted.title"))\n    aborted_games=list_games(conn,"aborted")\n    if not aborted_games:\n        st.info(tr("settings.aborted.none"))\n    else:\n        aborted_labels={\n            tr(\n                "settings.aborted.option",\n                round_name=g["round_name"],\n                course_code=g["course_code"],\n                team1=g["team1_points"],\n                team2=g["team2_points"],\n            ):int(g["id"])\n            for g in aborted_games\n        }\n        aborted_label=st.selectbox(\n            tr("settings.aborted.select"),\n            list(aborted_labels),\n            key="settings_aborted_select",\n        )\n        aborted_id=aborted_labels[aborted_label]\n        aborted_game=next(g for g in aborted_games if int(g["id"])==aborted_id)\n        delete_confirm_key=f"delete_aborted_confirm_{aborted_id}"\n        if st.button(tr("settings.aborted.delete"),key=f"delete_aborted_{aborted_id}",type="secondary"):\n            st.session_state[delete_confirm_key]=True\n            rerun()\n        if st.session_state.get(delete_confirm_key):\n            st.warning(tr(\n                "settings.aborted.warning",\n                round_name=aborted_game["round_name"],\n                course_code=aborted_game["course_code"],\n            ))\n            delete_yes,delete_no=st.columns(2)\n            if delete_yes.button(tr("settings.aborted.confirm"),key=f"delete_aborted_confirm_btn_{aborted_id}",type="primary"):\n                try:\n                    deleted_round=aborted_game["round_name"]\n                    deleted_course=aborted_game["course_code"]\n                    delete_aborted_game(conn,aborted_id)\n                    st.session_state.pop(delete_confirm_key,None)\n                    st.session_state["game_delete_success"]={"round_name":deleted_round,"course_code":deleted_course}\n                    rerun()\n                except Exception as e:\n                    show_error(e)\n            if delete_no.button(tr("settings.aborted.cancel"),key=f"delete_aborted_cancel_{aborted_id}"):\n                st.session_state.pop(delete_confirm_key,None)\n                rerun()\n\n'''
        text = insert_before_once(text, anchor, insertion, aborted_settings_marker, "Instructor Settings aborted games")

    path.write_text(text, encoding="utf-8")


def patch_locale(path: Path, values: dict[str, str]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in values.items():
        if data.get(key) != value:
            data[key] = value
            changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_locales() -> None:
    en = {
        "status.aborted": "Aborted",
        "question_log.coverage.aborted": "Aborted",
        "game.abort.button": "Abort game",
        "game.abort.warning": "Abort {round_name} · {course_code}? The game will no longer be treated as ongoing or regularly completed and cannot be resumed.",
        "game.abort.confirm": "Confirm abort",
        "game.abort.cancel": "Cancel",
        "game.abort.success": "The game {round_name} · {course_code} was aborted. You can delete it below.",
        "settings.aborted.title": "Aborted games",
        "settings.aborted.none": "There are no aborted games.",
        "settings.aborted.select": "Select aborted game",
        "settings.aborted.option": "{round_name} · {course_code} · {team1}:{team2}",
        "settings.aborted.delete": "Delete game",
        "settings.aborted.warning": "Delete {round_name} · {course_code}? The game and all data belonging exclusively to it will be permanently deleted. The round will then be open again for this course.",
        "settings.aborted.confirm": "Confirm deletion",
        "settings.aborted.cancel": "Cancel",
        "settings.aborted.deleted": "The aborted game {round_name} · {course_code} was deleted. The round is open again for this course.",
        "error.game.abort_not_found": "The game to be aborted was not found.",
        "error.game.abort_running_only": "Only an ongoing game can be aborted.",
        "error.game.delete_not_found": "The game to be deleted was not found.",
        "error.game.delete_aborted_only": "Only an aborted game can be deleted using this function.",
    }
    de = {
        "status.aborted": "Abgebrochen",
        "question_log.coverage.aborted": "Abgebrochen",
        "game.abort.button": "Spiel abbrechen",
        "game.abort.warning": "{round_name} · {course_code} abbrechen? Das Spiel gilt danach weder als laufend noch als regulär abgeschlossen und kann nicht fortgesetzt werden.",
        "game.abort.confirm": "Abbruch bestätigen",
        "game.abort.cancel": "Abbrechen",
        "game.abort.success": "Das Spiel {round_name} · {course_code} wurde abgebrochen. Es kann unten gelöscht werden.",
        "settings.aborted.title": "Abgebrochene Spiele",
        "settings.aborted.none": "Es sind keine abgebrochenen Spiele vorhanden.",
        "settings.aborted.select": "Abgebrochenes Spiel auswählen",
        "settings.aborted.option": "{round_name} · {course_code} · {team1}:{team2}",
        "settings.aborted.delete": "Spiel löschen",
        "settings.aborted.warning": "{round_name} · {course_code} löschen? Das Spiel und alle ausschließlich diesem Spiel zugeordneten Daten werden dauerhaft gelöscht. Die Runde gilt für diesen Kurs anschließend wieder als offen.",
        "settings.aborted.confirm": "Löschung bestätigen",
        "settings.aborted.cancel": "Abbrechen",
        "settings.aborted.deleted": "Das abgebrochene Spiel {round_name} · {course_code} wurde gelöscht. Die Runde gilt für diesen Kurs wieder als offen.",
        "error.game.abort_not_found": "Das abzubrechende Spiel wurde nicht gefunden.",
        "error.game.abort_running_only": "Nur ein laufendes Spiel kann abgebrochen werden.",
        "error.game.delete_not_found": "Das zu löschende Spiel wurde nicht gefunden.",
        "error.game.delete_aborted_only": "Über diese Funktion können ausschließlich abgebrochene Spiele gelöscht werden.",
    }
    patch_locale(ROOT / "locales" / "en.json", en)
    patch_locale(ROOT / "locales" / "de.json", de)


def write_tests() -> None:
    path = ROOT / "test_game_abort.py"
    content = '''import tempfile\nimport unittest\nfrom pathlib import Path\n\nfrom storage import (\n    StorageError,\n    abort_game,\n    add_learning_unit,\n    add_question,\n    add_student,\n    connect,\n    course_scoreboard,\n    create_course,\n    create_round,\n    dashboard_round_status,\n    delete_aborted_game,\n    game_cards,\n    get_game,\n    list_games,\n    randomize_teams,\n    start_game,\n)\n\n\nclass AbortDeleteGameTest(unittest.TestCase):\n    def setUp(self):\n        self.tmp = tempfile.TemporaryDirectory()\n        self.conn = connect(Path(self.tmp.name) / "test.sqlite3")\n\n    def tearDown(self):\n        self.conn.close()\n        self.tmp.cleanup()\n\n    def prepare_game(self):\n        create_course(self.conn, "WIBE225")\n        cid = self.conn.execute("SELECT id FROM courses WHERE code='WIBE225'").fetchone()[0]\n        add_learning_unit(self.conn, "LE1", "Test", 1)\n        uid = self.conn.execute("SELECT id FROM learning_units WHERE code='LE1'").fetchone()[0]\n        qids = []\n        for i in range(8):\n            add_question(self.conn, uid, f"Question {i+1}", f"Answer {i+1}")\n            qids.append(self.conn.execute("SELECT last_insert_rowid()").fetchone()[0])\n        rid = create_round(self.conn, "Round 1", qids)\n        for i in range(8):\n            add_student(self.conn, cid, f"Student {i+1}")\n        randomize_teams(self.conn, cid)\n        students = [r["id"] for r in self.conn.execute("SELECT id FROM students ORDER BY id").fetchall()]\n        gid = start_game(self.conn, rid, cid, students)\n        return cid, rid, gid, students\n\n    def test_running_game_can_be_aborted_and_is_not_running_afterwards(self):\n        cid, rid, gid, _ = self.prepare_game()\n        abort_game(self.conn, gid)\n        self.assertEqual(get_game(self.conn, gid)["status"], "aborted")\n        self.assertEqual(list_games(self.conn, "running"), [])\n        self.assertEqual([g["id"] for g in list_games(self.conn, "aborted")], [gid])\n        coverage = next(r for r in dashboard_round_status(self.conn) if int(r["id"]) == int(rid))\n        self.assertEqual(coverage["coverage"]["WIBE225"], "aborted")\n\n    def test_aborted_game_is_excluded_from_results(self):\n        cid, _, gid, _ = self.prepare_game()\n        self.conn.execute("UPDATE games SET team1_points=3,team2_points=2 WHERE id=?", (gid,))\n        self.conn.commit()\n        abort_game(self.conn, gid)\n        score = next(r for r in course_scoreboard(self.conn) if int(r["id"]) == int(cid))\n        self.assertEqual((score["team1_points"], score["team2_points"]), (0, 0))\n        self.assertEqual(int(score["games_played"] or 0), 0)\n\n    def test_only_running_games_can_be_aborted(self):\n        _, _, gid, _ = self.prepare_game()\n        self.conn.execute("UPDATE games SET status='finished' WHERE id=?", (gid,))\n        self.conn.commit()\n        with self.assertRaises(StorageError) as ctx:\n            abort_game(self.conn, gid)\n        self.assertEqual(ctx.exception.code, "error.game.abort_running_only")\n\n    def test_only_aborted_games_can_be_deleted(self):\n        _, _, gid, _ = self.prepare_game()\n        with self.assertRaises(StorageError) as ctx:\n            delete_aborted_game(self.conn, gid)\n        self.assertEqual(ctx.exception.code, "error.game.delete_aborted_only")\n        self.assertIsNotNone(get_game(self.conn, gid))\n\n    def test_delete_aborted_game_cascades_and_round_can_be_started_again(self):\n        cid, rid, gid, students = self.prepare_game()\n        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_roster WHERE game_id=?", (gid,)).fetchone()[0], 8)\n        self.assertEqual(len(game_cards(self.conn, gid)), 9)\n        abort_game(self.conn, gid)\n        delete_aborted_game(self.conn, gid)\n        self.assertIsNone(get_game(self.conn, gid))\n        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_roster WHERE game_id=?", (gid,)).fetchone()[0], 0)\n        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=?", (gid,)).fetchone()[0], 0)\n        coverage = next(r for r in dashboard_round_status(self.conn) if int(r["id"]) == int(rid))\n        self.assertEqual(coverage["coverage"]["WIBE225"], "open")\n        replacement = start_game(self.conn, rid, cid, students)\n        self.assertNotEqual(replacement, gid)\n        self.assertEqual(get_game(self.conn, replacement)["status"], "running")\n\n\nif __name__ == "__main__":\n    unittest.main()\n'''
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def main() -> None:
    patch_storage()
    patch_app()
    patch_locales()
    write_tests()
    print("US #26 patch applied successfully.")


if __name__ == "__main__":
    main()
