import csv
import io
import json
import random
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


QUESTION_POOL_FORMAT = "Syzeteo question pool"
CARD_TYPE_CHALLENGE = "challenge"


class StorageError(ValueError):
    """Language-neutral storage/domain error rendered by the UI translation layer."""

    def __init__(self, message_key: str, **params):
        super().__init__(message_key)
        self.code = message_key
        self.params = params


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: Path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    ensure_tables(conn)
    return conn


def ensure_tables(conn: sqlite3.Connection):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL DEFAULT '',
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS students (
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

        CREATE TABLE IF NOT EXISTS learning_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            position INTEGER NOT NULL DEFAULT 0,
            active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learning_unit_id INTEGER NOT NULL REFERENCES learning_units(id),
            question_text TEXT NOT NULL,
            answer_text TEXT NOT NULL DEFAULT '',
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rounds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            locked INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            locked_at TEXT
        );

        CREATE TABLE IF NOT EXISTS round_questions (
            round_id INTEGER NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
            question_id INTEGER NOT NULL,
            position INTEGER NOT NULL,
            question_text_snapshot TEXT,
            answer_text_snapshot TEXT,
            unit_code_snapshot TEXT,
            unit_title_snapshot TEXT,
            PRIMARY KEY(round_id, question_id),
            UNIQUE(round_id, position)
        );

        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            round_id INTEGER NOT NULL REFERENCES rounds(id),
            course_id INTEGER NOT NULL REFERENCES courses(id),
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

        CREATE TABLE IF NOT EXISTS game_roster (
            game_id INTEGER NOT NULL REFERENCES games(id) ON DELETE CASCADE,
            student_id INTEGER NOT NULL,
            display_name_snapshot TEXT NOT NULL,
            team_snapshot INTEGER NOT NULL CHECK(team_snapshot IN (1,2)),
            has_played INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(game_id, student_id)
        );

        CREATE TABLE IF NOT EXISTS game_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL REFERENCES games(id) ON DELETE CASCADE,
            card_no INTEGER NOT NULL,
            card_type TEXT NOT NULL CHECK(card_type IN ('question','challenge')),
            question_id INTEGER,
            question_text_snapshot TEXT,
            answer_text_snapshot TEXT,
            unit_code_snapshot TEXT,
            revealed INTEGER NOT NULL DEFAULT 0,
            resolved INTEGER NOT NULL DEFAULT 0,
            revealed_at TEXT,
            resolved_at TEXT,
            answered_by_student_id INTEGER,
            team_assist_used INTEGER NOT NULL DEFAULT 0,
            points_team INTEGER,
            points_awarded INTEGER NOT NULL DEFAULT 0,
            UNIQUE(game_id, card_no)
        );

        CREATE TABLE IF NOT EXISTS game_undo (
            game_id INTEGER PRIMARY KEY REFERENCES games(id) ON DELETE CASCADE,
            snapshot_json TEXT NOT NULL,
            action_label TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS app_settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT NOT NULL
        );
        """
    )
    # Syzeteo 1.0.0 introduces persistent UI settings.
    # Schema version 2 adds app_settings without changing existing domain tables.
    current_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
    if current_version < 2:
        conn.execute("PRAGMA user_version=2")
    conn.commit()


def get_app_setting(conn: sqlite3.Connection, key: str, default=None):
    row = conn.execute(
        "SELECT setting_value FROM app_settings WHERE setting_key=?",
        (str(key),),
    ).fetchone()
    return row[0] if row is not None else default


def set_app_setting(conn: sqlite3.Connection, key: str, value: str):
    conn.execute(
        """
        INSERT INTO app_settings(setting_key, setting_value) VALUES(?, ?)
        ON CONFLICT(setting_key) DO UPDATE SET setting_value=excluded.setting_value
        """,
        (str(key), str(value)),
    )
    conn.commit()



def dashboard_system_status(conn: sqlite3.Connection):
    """Liefert ausschließlich lesende Kennzahlen für die Instructor Settings."""
    integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    return {
        "database_ok": integrity == "ok",
        "database_status": integrity,
        "courses": conn.execute("SELECT COUNT(*) FROM courses WHERE active=1").fetchone()[0],
        "students": conn.execute(
            """
            SELECT COUNT(*)
            FROM students s JOIN courses c ON c.id=s.course_id
            WHERE s.active=1 AND c.active=1
            """
        ).fetchone()[0],
        "learning_units": conn.execute("SELECT COUNT(*) FROM learning_units WHERE active=1").fetchone()[0],
        "questions_active": conn.execute("SELECT COUNT(*) FROM questions WHERE active=1").fetchone()[0],
        "questions_archived": conn.execute("SELECT COUNT(*) FROM questions WHERE active=0").fetchone()[0],
        "rounds": conn.execute("SELECT COUNT(*) FROM rounds").fetchone()[0],
        "running_games": conn.execute("SELECT COUNT(*) FROM games WHERE status='running'").fetchone()[0],
    }


def dashboard_course_status(conn: sqlite3.Connection, course_id):
    course = conn.execute("SELECT * FROM courses WHERE id=?", (int(course_id),)).fetchone()
    if not course:
        raise StorageError("error.course.not_found")
    counts = conn.execute(
        """
        SELECT
            SUM(CASE WHEN active=1 THEN 1 ELSE 0 END) students,
            SUM(CASE WHEN active=1 AND team=1 THEN 1 ELSE 0 END) team1,
            SUM(CASE WHEN active=1 AND team=2 THEN 1 ELSE 0 END) team2,
            SUM(CASE WHEN active=1 AND team IS NULL THEN 1 ELSE 0 END) unassigned
        FROM students WHERE course_id=?
        """,
        (int(course_id),),
    ).fetchone()
    running = conn.execute(
        """
        SELECT g.*,r.name round_name,c.code course_code
        FROM games g JOIN rounds r ON r.id=g.round_id JOIN courses c ON c.id=g.course_id
        WHERE g.course_id=? AND g.status='running'
        ORDER BY g.id DESC LIMIT 1
        """,
        (int(course_id),),
    ).fetchone()
    return {
        "id": course["id"],
        "code": course["code"],
        "title": course["title"],
        "students": int(counts["students"] or 0),
        "team1": int(counts["team1"] or 0),
        "team2": int(counts["team2"] or 0),
        "unassigned": int(counts["unassigned"] or 0),
        "running_game": running,
    }


def dashboard_learning_unit_status(conn: sqlite3.Connection):
    rows = conn.execute(
        """
        SELECT lu.id,lu.code,lu.title,lu.position,lu.active,
               SUM(CASE WHEN q.active=1 THEN 1 ELSE 0 END) active_questions,
               SUM(CASE WHEN q.active=0 THEN 1 ELSE 0 END) archived_questions,
               COUNT(q.id) total_questions
        FROM learning_units lu
        LEFT JOIN questions q ON q.learning_unit_id=lu.id
        GROUP BY lu.id
        ORDER BY lu.position,lu.code
        """
    ).fetchall()
    return [dict(r) for r in rows]


def dashboard_round_status(conn: sqlite3.Connection):
    rounds = list_rounds(conn)
    courses = list_courses(conn)
    games = list_games(conn)
    game_by_pair = {(int(g["round_id"]), int(g["course_id"])): g for g in games}
    result = []
    for rnd in rounds:
        coverage = {}
        for course in courses:
            game = game_by_pair.get((int(rnd["id"]), int(course["id"])))
            if not game:
                coverage[course["code"]] = "open"
            elif game["status"] == "finished":
                coverage[course["code"]] = "played"
            elif game["status"] == "running":
                coverage[course["code"]] = "running"
            else:
                coverage[course["code"]] = game["status"]
        result.append({
            "id": rnd["id"],
            "name": rnd["name"],
            "n_questions": int(rnd["n_questions"] or 0),
            "locked": bool(rnd["locked"]),
            "playable": int(rnd["n_questions"] or 0) == 8,
            "coverage": coverage,
        })
    return result


def dashboard_configuration_issues(conn: sqlite3.Connection):
    """Return language-neutral configuration issue descriptors for Instructor Settings."""
    issues = []

    def add_issue(level, base_key, *, params=None, action_page=None, action_key=None):
        params = dict(params or {})
        issues.append({
            "level": level,
            "title_key": f"{base_key}.title",
            "title_params": params,
            "impact_key": f"{base_key}.impact",
            "impact_params": params,
            "solution_key": f"{base_key}.solution",
            "solution_params": params,
            "action_page": action_page,
            "action_key": action_key,
        })

    system = dashboard_system_status(conn)
    if not system["database_ok"]:
        add_issue(
            "error", "config.issue.db",
            params={"status": system["database_status"]},
        )

    courses = list_courses(conn)
    for course in courses:
        status = dashboard_course_status(conn, course["id"])
        if status["students"] == 0:
            add_issue(
                "warning", "config.issue.course_empty",
                params={"code": course["code"]},
                action_page="students", action_key="config.action.students",
            )
        if status["unassigned"]:
            add_issue(
                "warning", "config.issue.unassigned",
                params={"code": course["code"], "count": status["unassigned"]},
                action_page="students", action_key="config.action.students",
            )

    units = [u for u in dashboard_learning_unit_status(conn) if u["active"]]
    if not units:
        add_issue(
            "warning", "config.issue.no_unit",
            action_page="learning_units", action_key="config.action.learning_units",
        )
    for unit in units:
        if int(unit["active_questions"] or 0) == 0:
            add_issue(
                "warning", "config.issue.unit_no_questions",
                params={"code": unit["code"]},
                action_page="question_pool", action_key="config.action.question_pool",
            )

    rounds = dashboard_round_status(conn)
    for rnd in rounds:
        if not rnd["playable"]:
            add_issue(
                "warning", "config.issue.round_incomplete",
                params={"name": rnd["name"], "count": rnd["n_questions"]},
                action_page="rounds", action_key="config.action.rounds",
            )
    if not any(r["playable"] for r in rounds):
        add_issue(
            "warning", "config.issue.no_playable_round",
            action_page="rounds", action_key="config.action.rounds",
        )

    for game in list_games(conn, "running"):
        add_issue(
            "info", "config.issue.running",
            params={"round_name": game["round_name"], "course_code": game["course_code"]},
            action_page="game", action_key="config.action.game",
        )
    return issues

def create_course(conn, code: str, title: str = ""):
    code = (code or "").strip().upper()
    if not code:
        raise StorageError("course.error.code_required")
    try:
        conn.execute("INSERT INTO courses(code,title,created_at) VALUES(?,?,?)", (code, (title or "").strip(), now_iso()))
        conn.commit()
    except sqlite3.IntegrityError as exc:
        if "courses.code" in str(exc) or "UNIQUE constraint failed: courses.code" in str(exc):
            raise StorageError("course.error.code_exists", code=code) from exc
        raise


def list_courses(conn, active_only=True):
    where = "WHERE active=1" if active_only else ""
    return conn.execute(f"SELECT * FROM courses {where} ORDER BY code").fetchall()


def archive_course(conn, course_id):
    course = conn.execute("SELECT * FROM courses WHERE id=?", (int(course_id),)).fetchone()
    if not course:
        raise StorageError("course.error.not_found")
    if not course["active"]:
        return
    running = conn.execute(
        "SELECT COUNT(*) FROM games WHERE course_id=? AND status='running'",
        (int(course_id),),
    ).fetchone()[0]
    if running:
        raise StorageError("course.error.running_game")
    conn.execute("UPDATE courses SET active=0 WHERE id=?", (int(course_id),))
    conn.commit()


def reactivate_course(conn, course_id):
    course = conn.execute("SELECT * FROM courses WHERE id=?", (int(course_id),)).fetchone()
    if not course:
        raise StorageError("course.error.not_found")
    if course["active"]:
        return
    conn.execute("UPDATE courses SET active=1 WHERE id=?", (int(course_id),))
    conn.commit()


def delete_course(conn, course_id):
    course = conn.execute("SELECT * FROM courses WHERE id=?", (int(course_id),)).fetchone()
    if not course:
        raise StorageError("course.error.not_found")
    try:
        conn.execute("BEGIN")
        # Spiele zuerst löschen; game_roster und game_cards folgen per ON DELETE CASCADE.
        conn.execute("DELETE FROM games WHERE course_id=?", (int(course_id),))
        conn.execute("DELETE FROM students WHERE course_id=?", (int(course_id),))
        conn.execute("DELETE FROM courses WHERE id=?", (int(course_id),))
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def course_scoreboard(conn):
    return conn.execute(
        """
        SELECT c.id,c.code,c.title,
               COALESCE(SUM(CASE WHEN g.status='finished' THEN g.team1_points ELSE 0 END),0) team1_points,
               COALESCE(SUM(CASE WHEN g.status='finished' THEN g.team2_points ELSE 0 END),0) team2_points,
               SUM(CASE WHEN g.status='finished' THEN 1 ELSE 0 END) games_played,
               SUM(CASE WHEN g.status='finished' AND g.team1_points>g.team2_points THEN 1 ELSE 0 END) team1_wins,
               SUM(CASE WHEN g.status='finished' AND g.team2_points>g.team1_points THEN 1 ELSE 0 END) team2_wins,
               SUM(CASE WHEN g.status='finished' AND g.team1_points=g.team2_points THEN 1 ELSE 0 END) draws
        FROM courses c LEFT JOIN games g ON g.course_id=c.id
        WHERE c.active=1 GROUP BY c.id ORDER BY c.code
        """
    ).fetchall()


def list_students(conn, course_id, active_only=False):
    where = "AND active=1" if active_only else ""
    return conn.execute(
        f"SELECT * FROM students WHERE course_id=? {where} ORDER BY team,display_name", (course_id,)
    ).fetchall()


def add_student(conn, course_id, display_name, first_name="", last_name="", team=None):
    display_name = (display_name or "").strip()
    if not display_name:
        raise StorageError("error.student.name_required")
    conn.execute(
        "INSERT INTO students(course_id,first_name,last_name,display_name,team,created_at) VALUES(?,?,?,?,?,?)",
        (course_id, (first_name or "").strip(), (last_name or "").strip(), display_name, team, now_iso()),
    )
    conn.commit()


def import_students_csv(conn, course_id, raw: bytes):
    text = raw.decode("utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=";,\t,")
        sep = dialect.delimiter
    except csv.Error:
        sep = ";"
    df = pd.read_csv(io.StringIO(text), sep=sep, dtype=str).fillna("")
    cols = {str(c).strip().lower(): c for c in df.columns}
    imported = skipped = 0
    for _, row in df.iterrows():
        first = last = ""
        if "name" in cols:
            display = str(row[cols["name"]]).strip()
        elif "vorname" in cols and "nachname" in cols:
            first = str(row[cols["vorname"]]).strip()
            last = str(row[cols["nachname"]]).strip()
            display = f"{first} {last}".strip()
        elif "first_name" in cols and "last_name" in cols:
            first = str(row[cols["first_name"]]).strip()
            last = str(row[cols["last_name"]]).strip()
            display = f"{first} {last}".strip()
        else:
            raise StorageError("error.student.csv_columns")
        if not display:
            continue
        try:
            add_student(conn, course_id, display, first, last)
            imported += 1
        except sqlite3.IntegrityError:
            skipped += 1
    return imported, skipped


def randomize_teams(conn, course_id):
    rows = list_students(conn, course_id, active_only=True)
    if len(rows) < 2:
        raise StorageError("error.student.need_two")
    ids = [r["id"] for r in rows]
    random.SystemRandom().shuffle(ids)
    for idx, sid in enumerate(ids):
        team = 1 if idx % 2 == 0 else 2
        conn.execute("UPDATE students SET team=? WHERE id=?", (team, sid))
    conn.commit()


def update_student(conn, student_id, display_name, team, active):
    display_name = (display_name or "").strip()
    if not display_name:
        raise StorageError("error.student.name_required")
    if team not in (None, 1, 2):
        raise StorageError("error.student.invalid_team")
    conn.execute("UPDATE students SET display_name=?,team=?,active=? WHERE id=?", (display_name, team, int(bool(active)), student_id))
    conn.commit()


def add_learning_unit(conn, code, title, position=0):
    code = (code or "").strip().upper()
    title = (title or "").strip()
    if not code or not title:
        raise StorageError("error.learning_unit.required")
    conn.execute("INSERT INTO learning_units(code,title,position) VALUES(?,?,?)", (code,title,int(position)))
    conn.commit()


def update_learning_unit(conn, unit_id, code, title, position):
    code = (code or "").strip().upper()
    title = (title or "").strip()
    if not code or not title:
        raise StorageError("error.learning_unit.required")
    conn.execute(
        "UPDATE learning_units SET code=?,title=?,position=? WHERE id=?",
        (code,title,int(position),int(unit_id)),
    )
    conn.commit()


def learning_unit_question_count(conn, unit_id):
    return conn.execute(
        "SELECT COUNT(*) FROM questions WHERE learning_unit_id=?", (int(unit_id),)
    ).fetchone()[0]


def delete_learning_unit(conn, unit_id):
    unit = conn.execute("SELECT * FROM learning_units WHERE id=?", (int(unit_id),)).fetchone()
    if not unit:
        raise StorageError("error.learning_unit.not_found")
    count = learning_unit_question_count(conn, unit_id)
    if count:
        raise StorageError("error.learning_unit.in_use", count=count)
    conn.execute("DELETE FROM learning_units WHERE id=?", (int(unit_id),))
    conn.commit()


def list_learning_units(conn, active_only=True):
    where = "WHERE active=1" if active_only else ""
    return conn.execute(f"SELECT * FROM learning_units {where} ORDER BY position,code").fetchall()


def add_question(conn, unit_id, question_text, answer_text):
    q = (question_text or "").strip()
    if not q:
        raise StorageError("error.question.text_required")
    ts = now_iso()
    conn.execute(
        "INSERT INTO questions(learning_unit_id,question_text,answer_text,created_at,updated_at) VALUES(?,?,?,?,?)",
        (unit_id,q,(answer_text or "").strip(),ts,ts),
    )
    conn.commit()


def update_question(conn, question_id, unit_id, question_text, answer_text, active):
    conn.execute(
        "UPDATE questions SET learning_unit_id=?,question_text=?,answer_text=?,active=?,updated_at=? WHERE id=?",
        (unit_id,(question_text or "").strip(),(answer_text or "").strip(),int(bool(active)),now_iso(),question_id),
    )
    conn.commit()


def delete_question(conn, question_id):
    qid = int(question_id)
    question = conn.execute(
        """
        SELECT q.*,lu.code unit_code,lu.title unit_title
        FROM questions q JOIN learning_units lu ON lu.id=q.learning_unit_id
        WHERE q.id=?
        """, (qid,)
    ).fetchone()
    if not question:
        raise StorageError("error.question.not_found")

    unlocked = conn.execute(
        """
        SELECT r.name
        FROM round_questions rq JOIN rounds r ON r.id=rq.round_id
        WHERE rq.question_id=? AND r.locked=0
        ORDER BY r.id
        """, (qid,)
    ).fetchall()
    if unlocked:
        names = ", ".join(r["name"] for r in unlocked)
        raise StorageError("error.question.in_editable_round", names=names)

    # Für bereits gesperrte Runden den historischen Stand sicher in den Snapshots
    # hinterlegen, bevor die Frage aus dem globalen Pool entfernt wird.
    conn.execute(
        """
        UPDATE round_questions
        SET question_text_snapshot=COALESCE(question_text_snapshot,?),
            answer_text_snapshot=COALESCE(answer_text_snapshot,?),
            unit_code_snapshot=COALESCE(unit_code_snapshot,?),
            unit_title_snapshot=COALESCE(unit_title_snapshot,?)
        WHERE question_id=?
        """,
        (question["question_text"],question["answer_text"],question["unit_code"],question["unit_title"],qid),
    )
    conn.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()


def list_questions(conn, active_only=False):
    where = "WHERE q.active=1" if active_only else ""
    return conn.execute(
        f"""
        SELECT q.*,lu.code unit_code,lu.title unit_title
        FROM questions q JOIN learning_units lu ON lu.id=q.learning_unit_id
        {where} ORDER BY lu.position,lu.code,q.id
        """
    ).fetchall()




def _normalize_question_text(text):
    return " ".join((text or "").split()).casefold()


def export_question_pool_json(conn):
    """Exportiert ausschließlich Lerneinheiten und Fragen, ohne IDs oder Spieldaten."""
    units = list_learning_units(conn, False)
    questions = list_questions(conn, False)
    payload = {
        "format": QUESTION_POOL_FORMAT,
        "version": 1,
        "exported_at": now_iso(),
        "learning_units": [
            {
                "code": u["code"],
                "title": u["title"],
                "position": int(u["position"]),
                "active": bool(u["active"]),
            }
            for u in units
        ],
        "questions": [
            {
                "learning_unit": q["unit_code"],
                "question": q["question_text"],
                "answer": q["answer_text"],
                "active": bool(q["active"]),
            }
            for q in questions
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def export_question_pool_csv(conn):
    """Lesbarer CSV-Export für Excel; Import zwischen Syzeteo-Instanzen erfolgt über JSON."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";", lineterminator="\n")
    writer.writerow([
        "le_code", "le_titel", "sortierung", "le_aktiv",
        "frage", "musterantwort", "frage_aktiv",
    ])
    units = list_learning_units(conn, False)
    questions_by_unit = {}
    for q in list_questions(conn, False):
        questions_by_unit.setdefault(q["learning_unit_id"], []).append(q)
    for unit in units:
        unit_questions = questions_by_unit.get(unit["id"], [])
        if not unit_questions:
            writer.writerow([
                unit["code"], unit["title"], int(unit["position"]), int(bool(unit["active"])),
                "", "", "",
            ])
            continue
        for q in unit_questions:
            writer.writerow([
                unit["code"], unit["title"], int(unit["position"]), int(bool(unit["active"])),
                q["question_text"], q["answer_text"], int(bool(q["active"])),
            ])
    return ("\ufeff" + output.getvalue()).encode("utf-8")


def _parse_question_pool_import(raw):
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise StorageError("error.import.not_utf8") from exc
    else:
        text = str(raw)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise StorageError("error.import.invalid_json") from exc

    if not isinstance(payload, dict):
        raise StorageError("error.import.invalid_format")
    if payload.get("format") != QUESTION_POOL_FORMAT:
        raise StorageError("error.import.unsupported_pool")
    if payload.get("version") != 1:
        raise StorageError("error.import.unsupported_version")

    units_raw = payload.get("learning_units")
    questions_raw = payload.get("questions")
    if not isinstance(units_raw, list) or not isinstance(questions_raw, list):
        raise StorageError("error.import.missing_lists")

    units = []
    seen_codes = set()
    for idx, item in enumerate(units_raw, start=1):
        if not isinstance(item, dict):
            raise StorageError("error.import.invalid_unit", index=idx)
        code = (item.get("code") or "").strip().upper()
        title = (item.get("title") or "").strip()
        if not code or not title:
            raise StorageError("error.import.unit_required", index=idx)
        if code in seen_codes:
            raise StorageError("error.import.duplicate_unit_code", code=code)
        seen_codes.add(code)
        try:
            position = int(item.get("position", 0))
        except (TypeError, ValueError) as exc:
            raise StorageError("error.import.invalid_position", code=code) from exc
        units.append({
            "code": code,
            "title": title,
            "position": position,
            "active": bool(item.get("active", True)),
        })

    questions = []
    for idx, item in enumerate(questions_raw, start=1):
        if not isinstance(item, dict):
            raise StorageError("error.import.invalid_question", index=idx)
        code = (item.get("learning_unit") or "").strip().upper()
        question = (item.get("question") or "").strip()
        answer = (item.get("answer") or "").strip()
        if not code or not question:
            raise StorageError("error.import.question_required", index=idx)
        questions.append({
            "learning_unit": code,
            "question": question,
            "answer": answer,
            "active": bool(item.get("active", True)),
        })
    return units, questions


def preview_question_pool_import(conn, raw):
    """Prüft einen Import ohne irgendeine Änderung an der Datenbank."""
    units, questions = _parse_question_pool_import(raw)
    existing_units = {u["code"].upper(): u for u in list_learning_units(conn, False)}
    import_codes = {u["code"] for u in units}

    missing_codes = sorted({q["learning_unit"] for q in questions} - set(existing_units) - import_codes)
    if missing_codes:
        raise StorageError("error.import.missing_units", codes=", ".join(missing_codes))

    conflicts = []
    new_units = 0
    reused_units = 0
    for unit in units:
        existing = existing_units.get(unit["code"])
        if existing:
            reused_units += 1
            if (existing["title"] != unit["title"] or int(existing["position"]) != unit["position"]):
                conflicts.append({
                    "code": unit["code"],
                    "existing_title": existing["title"],
                    "import_title": unit["title"],
                    "existing_position": int(existing["position"]),
                    "import_position": unit["position"],
                })
        else:
            new_units += 1

    seen_questions = {_normalize_question_text(q["question_text"]) for q in list_questions(conn, False)}
    new_questions = 0
    duplicate_questions = 0
    for q in questions:
        key = _normalize_question_text(q["question"])
        if key in seen_questions:
            duplicate_questions += 1
        else:
            new_questions += 1
            seen_questions.add(key)

    return {
        "learning_units_total": len(units),
        "questions_total": len(questions),
        "new_units": new_units,
        "reused_units": reused_units,
        "unit_conflicts": conflicts,
        "new_questions": new_questions,
        "duplicate_questions": duplicate_questions,
    }


def import_question_pool_json(conn, raw):
    """Ergänzt nur neue Inhalte. Bestehende Datensätze werden niemals überschrieben."""
    units, questions = _parse_question_pool_import(raw)
    # Vorab vollständig validieren, ohne Änderungen vorzunehmen.
    preview_question_pool_import(conn, raw)
    try:
        conn.execute("BEGIN")
        existing_units = {
            row["code"].upper(): row
            for row in conn.execute("SELECT * FROM learning_units").fetchall()
        }
        added_units = 0
        for unit in units:
            if unit["code"] in existing_units:
                continue
            conn.execute(
                "INSERT INTO learning_units(code,title,position,active) VALUES(?,?,?,?)",
                (unit["code"], unit["title"], unit["position"], int(unit["active"])),
            )
            added_units += 1

        unit_ids = {
            row["code"].upper(): row["id"]
            for row in conn.execute("SELECT id,code FROM learning_units").fetchall()
        }
        seen_questions = {
            _normalize_question_text(row["question_text"])
            for row in conn.execute("SELECT question_text FROM questions").fetchall()
        }
        added_questions = 0
        skipped_questions = 0
        ts = now_iso()
        for q in questions:
            key = _normalize_question_text(q["question"])
            if key in seen_questions:
                skipped_questions += 1
                continue
            conn.execute(
                """
                INSERT INTO questions(
                    learning_unit_id,question_text,answer_text,active,created_at,updated_at
                ) VALUES(?,?,?,?,?,?)
                """,
                (unit_ids[q["learning_unit"]], q["question"], q["answer"], int(q["active"]), ts, ts),
            )
            added_questions += 1
            seen_questions.add(key)
        conn.commit()
        return {
            "added_units": added_units,
            "added_questions": added_questions,
            "skipped_questions": skipped_questions,
        }
    except Exception:
        conn.rollback()
        raise


def create_round(conn, name, question_ids):
    name = (name or "").strip()
    qids = list(dict.fromkeys(int(x) for x in question_ids))
    if not name:
        raise StorageError("error.round.name_required")
    if len(qids) != 8:
        raise StorageError("error.round.exact_eight")
    placeholders=",".join("?" for _ in qids)
    existing=conn.execute(f"SELECT COUNT(*) FROM questions WHERE id IN ({placeholders})", qids).fetchone()[0]
    if existing != len(qids):
        raise StorageError("error.round.question_missing")
    conn.execute("INSERT INTO rounds(name,created_at) VALUES(?,?)", (name,now_iso()))
    rid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    for pos,qid in enumerate(qids, start=1):
        conn.execute("INSERT INTO round_questions(round_id,question_id,position) VALUES(?,?,?)", (rid,qid,pos))
    conn.commit()
    return rid


def list_rounds(conn):
    return conn.execute(
        """
        SELECT r.*,COUNT(rq.question_id) n_questions
        FROM rounds r LEFT JOIN round_questions rq ON rq.round_id=r.id
        GROUP BY r.id ORDER BY r.id DESC
        """
    ).fetchall()


def round_questions(conn, round_id):
    return conn.execute(
        """
        SELECT rq.*,
               COALESCE(rq.question_text_snapshot,q.question_text) question_text,
               COALESCE(rq.answer_text_snapshot,q.answer_text) answer_text,
               COALESCE(rq.unit_code_snapshot,lu.code) unit_code,
               COALESCE(rq.unit_title_snapshot,lu.title) unit_title
        FROM round_questions rq
        LEFT JOIN questions q ON q.id=rq.question_id
        LEFT JOIN learning_units lu ON lu.id=q.learning_unit_id
        WHERE rq.round_id=? ORDER BY rq.position
        """, (round_id,)
    ).fetchall()


def update_round_questions(conn, round_id, question_ids):
    row = conn.execute("SELECT locked FROM rounds WHERE id=?", (round_id,)).fetchone()
    if not row:
        raise StorageError("error.round.not_found")
    if row["locked"]:
        raise StorageError("error.round.locked")
    qids = list(dict.fromkeys(int(x) for x in question_ids))
    if len(qids) != 8:
        raise StorageError("error.round.exact_eight")
    placeholders=",".join("?" for _ in qids)
    existing=conn.execute(f"SELECT COUNT(*) FROM questions WHERE id IN ({placeholders})", qids).fetchone()[0]
    if existing != len(qids):
        raise StorageError("error.round.question_missing")
    conn.execute("DELETE FROM round_questions WHERE round_id=?", (round_id,))
    for pos,qid in enumerate(qids, start=1):
        conn.execute("INSERT INTO round_questions(round_id,question_id,position) VALUES(?,?,?)", (round_id,qid,pos))
    conn.commit()


def lock_round(conn, round_id):
    row = conn.execute("SELECT locked FROM rounds WHERE id=?", (round_id,)).fetchone()
    if row is None:
        raise StorageError("error.round.not_found")
    if row["locked"]:
        return
    rows = round_questions(conn, round_id)
    if len(rows) != 8:
        raise StorageError("error.round.exact_eight")
    for r in rows:
        conn.execute(
            """
            UPDATE round_questions SET question_text_snapshot=?,answer_text_snapshot=?,unit_code_snapshot=?,unit_title_snapshot=?
            WHERE round_id=? AND question_id=?
            """,
            (r["question_text"],r["answer_text"],r["unit_code"],r["unit_title"],round_id,r["question_id"]),
        )
    conn.execute("UPDATE rounds SET locked=1,locked_at=? WHERE id=?", (now_iso(),round_id))
    conn.commit()


def start_game(conn, round_id, course_id, present_student_ids, first_player_mode="random", first_player_id=None, player_selection_mode="random"):

    existing = conn.execute("SELECT id FROM games WHERE round_id=? AND course_id=?", (round_id,course_id)).fetchone()
    if existing:
        raise StorageError("error.round.started_course")
    first_player_mode = (first_player_mode or "random").strip().lower()
    if first_player_mode not in ("manual", "random"):
        raise StorageError("error.game.invalid_starter_mode")
    player_selection_mode = (player_selection_mode or "random").strip().lower()
    if player_selection_mode not in ("manual", "random"):
        raise StorageError("error.game.invalid_player_mode")
    roster = []
    for sid in present_student_ids:
        student = conn.execute("SELECT * FROM students WHERE id=? AND course_id=? AND active=1", (int(sid),course_id)).fetchone()
        if student and student["team"] in (1,2):
            roster.append(student)
    if not roster:
        raise StorageError("error.game.no_present")
    team1_count=sum(1 for r in roster if r["team"]==1)
    team2_count=sum(1 for r in roster if r["team"]==2)
    if team1_count < 4 or team2_count < 4:
        raise StorageError("error.game.need_four")

    if first_player_mode == "manual":
        if first_player_id is None:
            raise StorageError("error.game.starter_required")
        starter = next((r for r in roster if int(r["id"]) == int(first_player_id)), None)
        if starter is None:
            raise StorageError("error.game.starter_not_present")
    else:
        starter = random.SystemRandom().choice(roster)

    # Erst nach erfolgreicher Startprüfung wird der gemeinsame Fragensatz gesperrt.
    lock_round(conn, round_id)
    # Der vor Spielbeginn festgelegte Modus wird pro Spiel eingefroren.
    # Damit bleibt die Einstellung während des laufenden Spiels unveränderlich.
    conn.execute(
        "INSERT INTO games(round_id,course_id,started_at,current_student_id,current_team,player_selection_mode) VALUES(?,?,?,?,?,?)",
        (round_id,course_id,now_iso(),starter["id"],starter["team"],player_selection_mode),
    )
    gid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    for student in roster:
        conn.execute(
            "INSERT INTO game_roster(game_id,student_id,display_name_snapshot,team_snapshot,has_played) VALUES(?,?,?,?,?)",
            (gid,student["id"],student["display_name"],student["team"],int(student["id"]==starter["id"])),
        )
    rq = conn.execute(
        "SELECT * FROM round_questions WHERE round_id=? ORDER BY position", (round_id,)
    ).fetchall()
    cards=[]
    for q in rq:
        cards.append({
            "type":"question","qid":q["question_id"],"q":q["question_text_snapshot"],
            "a":q["answer_text_snapshot"],"u":q["unit_code_snapshot"]
        })
    cards.append({"type":CARD_TYPE_CHALLENGE,"qid":None,"q":None,"a":None,"u":None})
    random.SystemRandom().shuffle(cards)
    for no,card in enumerate(cards,start=1):
        conn.execute(
            """
            INSERT INTO game_cards(game_id,card_no,card_type,question_id,question_text_snapshot,answer_text_snapshot,unit_code_snapshot)
            VALUES(?,?,?,?,?,?,?)
            """,
            (gid,no,card["type"],card["qid"],card["q"],card["a"],card["u"]),
        )
    conn.commit()
    return gid


def get_game(conn, game_id):
    return conn.execute(
        """
        SELECT g.*,r.name round_name,c.code course_code
        FROM games g JOIN rounds r ON r.id=g.round_id JOIN courses c ON c.id=g.course_id
        WHERE g.id=?
        """, (game_id,)
    ).fetchone()


def list_games(conn, status=None):
    where="WHERE g.status=?" if status else ""
    args=(status,) if status else ()
    return conn.execute(
        f"""
        SELECT g.*,r.name round_name,c.code course_code
        FROM games g JOIN rounds r ON r.id=g.round_id JOIN courses c ON c.id=g.course_id
        {where} ORDER BY g.id DESC
        """, args
    ).fetchall()


def game_cards(conn, game_id):
    return conn.execute("SELECT * FROM game_cards WHERE game_id=? ORDER BY card_no", (game_id,)).fetchall()


def game_roster(conn, game_id, team=None):
    if team:
        return conn.execute("SELECT * FROM game_roster WHERE game_id=? AND team_snapshot=? ORDER BY display_name_snapshot", (game_id,team)).fetchall()
    return conn.execute("SELECT * FROM game_roster WHERE game_id=? ORDER BY team_snapshot,display_name_snapshot", (game_id,)).fetchall()


def current_player(conn, game):
    if not game or not game["current_student_id"]:
        return None
    return conn.execute(
        "SELECT * FROM game_roster WHERE game_id=? AND student_id=?", (game["id"],game["current_student_id"])
    ).fetchone()


def change_start_player(conn, game_id, student_id):
    """Kompatibilitätsfunktion: Der erste Spieler wird ausschließlich vor Spielstart festgelegt."""
    raise StorageError("error.game.first_player_locked")


def _awaiting_next_player(conn, game):
    if not game or game["status"] != "running":
        return False
    open_card = conn.execute(
        "SELECT 1 FROM game_cards WHERE game_id=? AND revealed=1 AND resolved=0", (game["id"],)
    ).fetchone()
    if open_card:
        return False
    unresolved = conn.execute(
        "SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=0", (game["id"],)
    ).fetchone()[0]
    if unresolved <= 1:
        return False
    resolved = conn.execute(
        "SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=1", (game["id"],)
    ).fetchone()[0]
    return resolved >= int(game["turn_no"])


def _choose_random_next_player(conn, game):
    """Wählt ohne eigenen Undo-Snapshot den nächsten zulässigen regulären Spieler."""
    next_team = 2 if int(game["current_team"]) == 1 else 1
    candidates = conn.execute(
        "SELECT * FROM game_roster WHERE game_id=? AND team_snapshot=? AND has_played=0",
        (game["id"], next_team),
    ).fetchall()
    if not candidates:
        return None
    player = random.SystemRandom().choice(candidates)
    conn.execute(
        "UPDATE game_roster SET has_played=1 WHERE game_id=? AND student_id=?",
        (game["id"], int(player["student_id"])),
    )
    conn.execute(
        "UPDATE games SET current_student_id=?,current_team=?,turn_no=turn_no+1 WHERE id=?",
        (int(player["student_id"]), next_team, game["id"]),
    )
    return player


def add_late_player(conn, game_id, student_id):
    """Nimmt einen verspätet eintreffenden Studierenden in den laufenden Spielroster auf."""
    game = get_game(conn, game_id)
    if not game or game["status"] != "running":
        raise StorageError("error.game.late_running_only")
    existing = conn.execute(
        "SELECT 1 FROM game_roster WHERE game_id=? AND student_id=?", (game_id, int(student_id))
    ).fetchone()
    if existing:
        raise StorageError("error.game.already_roster")
    student = conn.execute(
        "SELECT * FROM students WHERE id=? AND course_id=? AND active=1",
        (int(student_id), int(game["course_id"])),
    ).fetchone()
    if not student or student["team"] not in (1, 2):
        raise StorageError("error.game.late_invalid")
    _save_undo_snapshot(conn, game_id, "undo.action.late_player")
    conn.execute(
        "INSERT INTO game_roster(game_id,student_id,display_name_snapshot,team_snapshot,has_played) VALUES(?,?,?,?,0)",
        (game_id, int(student["id"]), student["display_name"], int(student["team"])),
    )
    # Falls ein Zufallsspiel mangels Kandidat angehalten war und der neue Roster
    # nun einen zulässigen Kandidaten enthält, wird die Auswahl atomar mit der
    # Aufnahme abgeschlossen. Im manuellen Modus bleibt die Auswahl beim Instructor.
    refreshed = get_game(conn, game_id)
    if refreshed["player_selection_mode"] == "random" and _awaiting_next_player(conn, refreshed):
        _choose_random_next_player(conn, refreshed)
    conn.commit()


def _save_undo_snapshot(conn, game_id, action_key, action_params=None):
    game = conn.execute("SELECT * FROM games WHERE id=?", (game_id,)).fetchone()
    if not game:
        return
    payload = {
        "game": dict(game),
        "roster": [dict(r) for r in conn.execute("SELECT * FROM game_roster WHERE game_id=? ORDER BY student_id", (game_id,)).fetchall()],
        "cards": [dict(r) for r in conn.execute("SELECT * FROM game_cards WHERE game_id=? ORDER BY id", (game_id,)).fetchall()],
    }
    action_descriptor = json.dumps(
        {"key": action_key, "params": dict(action_params or {})},
        ensure_ascii=False, separators=(",", ":"),
    )
    conn.execute(
        """
        INSERT INTO game_undo(game_id,snapshot_json,action_label,created_at) VALUES(?,?,?,?)
        ON CONFLICT(game_id) DO UPDATE SET snapshot_json=excluded.snapshot_json,action_label=excluded.action_label,created_at=excluded.created_at
        """,
        (game_id,json.dumps(payload,ensure_ascii=False),action_descriptor,now_iso()),
    )
    conn.commit()

def undo_info(conn, game_id):
    row = conn.execute("SELECT action_label,created_at FROM game_undo WHERE game_id=?", (game_id,)).fetchone()
    if row is None:
        return None
    try:
        descriptor = json.loads(row["action_label"])
        return {
            "action_key": descriptor.get("key", "undo.action.score_card"),
            "action_params": descriptor.get("params") or {},
            "created_at": row["created_at"],
        }
    except (TypeError, json.JSONDecodeError):
        return {"action_key": "undo.action.score_card", "action_params": {}, "created_at": row["created_at"]}


def undo_last_action(conn, game_id):
    undo = conn.execute("SELECT * FROM game_undo WHERE game_id=?", (game_id,)).fetchone()
    if not undo:
        raise StorageError("error.undo.none")
    payload=json.loads(undo["snapshot_json"])
    game=payload["game"]
    try:
        conn.execute("BEGIN")
        columns=[r[1] for r in conn.execute("PRAGMA table_info(games)").fetchall() if r[1] != "id"]
        conn.execute(
            f"UPDATE games SET {','.join(f'{c}=?' for c in columns)} WHERE id=?",
            [game[c] for c in columns]+[game_id],
        )
        conn.execute("DELETE FROM game_roster WHERE game_id=?", (game_id,))
        for row in payload["roster"]:
            cols=list(row)
            conn.execute(
                f"INSERT INTO game_roster({','.join(cols)}) VALUES({','.join('?' for _ in cols)})",
                [row[c] for c in cols],
            )
        conn.execute("DELETE FROM game_cards WHERE game_id=?", (game_id,))
        for row in payload["cards"]:
            # Keine personenbezogene Leistungszuordnung wiederherstellen.
            row["answered_by_student_id"]=None
            cols=list(row)
            conn.execute(
                f"INSERT INTO game_cards({','.join(cols)}) VALUES({','.join('?' for _ in cols)})",
                [row[c] for c in cols],
            )
        conn.execute("DELETE FROM game_undo WHERE game_id=?", (game_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def reveal_card(conn, game_id, card_no):
    game = get_game(conn,game_id)
    if not game or game["status"] != "running":
        raise StorageError("error.game.not_running")
    unresolved = conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=0", (game_id,)).fetchone()[0]
    card = conn.execute("SELECT * FROM game_cards WHERE game_id=? AND card_no=?", (game_id,card_no)).fetchone()
    if not card or card["resolved"]:
        raise StorageError("error.card.unavailable")
    # Nur eine aufgedeckte, noch nicht gewertete Karte gleichzeitig.
    open_card = conn.execute("SELECT id FROM game_cards WHERE game_id=? AND revealed=1 AND resolved=0", (game_id,)).fetchone()
    if open_card and open_card["id"] != card["id"]:
        raise StorageError("error.card.score_open_first")
    # Nach jeder gewerteten Studentenkarte muss die Auswahl des nächsten
    # regulären Spielers abgeschlossen sein. Dabei wird turn_no erhöht.
    if not card["revealed"] and unresolved > 1 and not open_card:
        resolved = conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=1", (game_id,)).fetchone()[0]
        if resolved >= int(game["turn_no"]):
            raise StorageError("error.game.select_next_first")
    if not card["revealed"]:
        _save_undo_snapshot(conn,game_id,"undo.action.reveal_card", {"card_no": card_no})
        conn.execute("UPDATE game_cards SET revealed=1,revealed_at=? WHERE id=?", (now_iso(),card["id"]))
        conn.commit()
    return unresolved == 1


def resolve_question(conn, game_id, card_id, points, team_assist_used=False, answered_by_student_id=None):
    game = get_game(conn,game_id)
    card = conn.execute("SELECT * FROM game_cards WHERE id=? AND game_id=?", (card_id,game_id)).fetchone()
    if not game or not card or not card["revealed"] or card["resolved"]:
        raise StorageError("error.card.not_scorable")
    unresolved_before = conn.execute(
        "SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=0", (game_id,)
    ).fetchone()[0]
    team = game["current_team"]
    points = int(points)
    if points not in (0,1,2):
        raise StorageError("error.card.invalid_points")
    if card["card_type"] == "question" and points not in (0,1):
        raise StorageError("error.card.question_max_one")
    substitute = None
    col = None
    if team_assist_used:
        col = "team1_assist_used" if team==1 else "team2_assist_used"
        if game[col]:
            raise StorageError("error.assist.used")
        if not answered_by_student_id:
            raise StorageError("error.assist.person_required")
        substitute = conn.execute(
            "SELECT * FROM game_roster WHERE game_id=? AND student_id=? AND team_snapshot=?",
            (game_id,int(answered_by_student_id),team),
        ).fetchone()
        if not substitute:
            raise StorageError("error.assist.wrong_team")
    _save_undo_snapshot(conn,game_id,"undo.action.score_card")
    if team_assist_used:
        # A Team Assist is not a regular turn. The assisting person remains
        # eligible for a later regular turn in the same round (GR #05/#06).
        conn.execute(f"UPDATE games SET {col}=1 WHERE id=?", (game_id,))
    scorecol = "team1_points" if team==1 else "team2_points"
    conn.execute(f"UPDATE games SET {scorecol}={scorecol}+? WHERE id=?", (points,game_id))
    conn.execute(
        """
        UPDATE game_cards SET resolved=1,resolved_at=?,answered_by_student_id=?,team_assist_used=?,points_team=?,points_awarded=?
        WHERE id=?
        """,
        (now_iso(),None,int(bool(team_assist_used)),team if points else None,points,card_id),
    )
    # Im Zufallsmodus gehört die Auswahl des nächsten regulären Spielers fachlich
    # zur Wertung dieses Zuges und teilt deshalb denselben Undo-Snapshot. Im
    # manuellen Modus bleibt der Zustand bis zur Auswahl durch den Instructor offen.
    if unresolved_before > 2 and game["player_selection_mode"] == "random":
        _choose_random_next_player(conn, game)
    conn.commit()


def resolve_instructor_card(conn, game_id, card_id):
    card = conn.execute("SELECT * FROM game_cards WHERE id=? AND game_id=?", (card_id,game_id)).fetchone()
    if not card or not card["revealed"] or card["resolved"]:
        raise StorageError("error.card.not_finishable")
    unresolved = conn.execute("SELECT COUNT(*) FROM game_cards WHERE game_id=? AND resolved=0", (game_id,)).fetchone()[0]
    if unresolved != 1:
        raise StorageError("error.card.instructor_last_only")
    _save_undo_snapshot(conn,game_id,"undo.action.finish_game")
    conn.execute("UPDATE game_cards SET resolved=1,resolved_at=?,points_awarded=0 WHERE id=?", (now_iso(),card_id))
    conn.execute("UPDATE games SET status='finished',finished_at=?,current_student_id=NULL,current_team=NULL WHERE id=?", (now_iso(),game_id))
    conn.commit()


def set_next_player(conn, game_id, student_id):
    """Setzt im manuellen Modus den nächsten zulässigen regulären Spieler."""
    game = get_game(conn, game_id)
    if not game or game["status"] != "running":
        raise StorageError("error.game.not_running")
    if game["player_selection_mode"] != "manual":
        raise StorageError("error.game.manual_mode_off")
    if not _awaiting_next_player(conn, game):
        raise StorageError("error.game.next_not_required")

    next_team = 2 if int(game["current_team"]) == 1 else 1
    player = conn.execute(
        """
        SELECT * FROM game_roster
        WHERE game_id=? AND student_id=? AND team_snapshot=? AND has_played=0
        """,
        (game_id, int(student_id), next_team),
    ).fetchone()
    if not player:
        raise StorageError("error.game.next_unavailable")

    # Kein neuer Undo-Snapshot: Die manuelle Auswahl gehört – wie die Zufallsauswahl –
    # fachlich zur vorangegangenen Kartenwertung. Ein Undo setzt damit beides zurück.
    conn.execute(
        "UPDATE game_roster SET has_played=1 WHERE game_id=? AND student_id=?",
        (game_id, int(student_id)),
    )
    conn.execute(
        "UPDATE games SET current_student_id=?,current_team=?,turn_no=turn_no+1 WHERE id=?",
        (int(student_id), next_team, game_id),
    )
    conn.commit()
    return player


def protocol_rows(conn):
    # Tatsächlich aufgedeckte/gewertete Fachfragen; nicht nur für eine Runde geplante Fragen.
    return conn.execute(
        """
        SELECT r.id round_id,r.name round_name,
               gc.card_no position,gc.question_id,
               gc.unit_code_snapshot unit_code,
               gc.question_text_snapshot question_text,
               c.code course_code,g.started_at,g.finished_at,g.status,
               gc.resolved_at
        FROM game_cards gc
        JOIN games g ON g.id=gc.game_id
        JOIN rounds r ON r.id=g.round_id
        JOIN courses c ON c.id=g.course_id
        WHERE gc.card_type='question' AND gc.resolved=1
        ORDER BY g.started_at,r.id,g.id,gc.card_no
        """
    ).fetchall()


def game_history(conn, course_id=None):
    where="WHERE g.course_id=?" if course_id else ""
    args=(course_id,) if course_id else ()
    return conn.execute(
        f"""
        SELECT g.id,g.round_id,r.name round_name,c.code course_code,g.started_at,g.finished_at,g.status,g.team1_points,g.team2_points
        FROM games g JOIN rounds r ON r.id=g.round_id JOIN courses c ON c.id=g.course_id
        {where} ORDER BY g.id DESC
        """,args
    ).fetchall()
