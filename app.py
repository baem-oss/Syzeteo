import os
import textwrap

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from auth import authenticate, change_password, change_username, create_admin, user_count
from config import resolve_data_dir, resolve_database_path
from i18n import available_locales, initial_locale, locale_display_name, t
from storage import (
    add_late_player, add_learning_unit, add_question, add_student, archive_course, connect, course_scoreboard,
    abort_game, create_course, create_round, delete_aborted_game, delete_course, delete_learning_unit, delete_question,
    export_question_pool_csv, export_question_pool_json, game_cards, game_history, game_roster,
    get_game, import_question_pool_json, import_students_csv, learning_unit_question_count,
    list_courses, list_games, list_learning_units, list_questions, preview_question_pool_import,
    list_rounds, list_students, protocol_rows, randomize_teams, reveal_card,
    reactivate_course, round_questions, start_game, update_learning_unit, update_question,
    update_round_questions, update_student, current_player, resolve_instructor_card,
    resolve_question, set_next_player, undo_info, undo_last_action,
    dashboard_system_status, dashboard_course_status, dashboard_learning_unit_status,
    dashboard_round_status, dashboard_configuration_issues, CARD_TYPE_CHALLENGE,
    get_app_setting, set_app_setting, StorageError,
)

APP_VERSION = "1.1.0-dev1"

st.set_page_config(page_title="Syzeteo", page_icon="🧠", layout="wide")

DATA_DIR = resolve_data_dir()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = resolve_database_path(DATA_DIR)
conn = connect(DB_PATH)

PAGE_DASHBOARD = "dashboard"
PAGE_COURSES = "courses"
PAGE_STUDENTS = "students"
PAGE_LEARNING_UNITS = "learning_units"
PAGE_QUESTION_POOL = "question_pool"
PAGE_IMPORT_EXPORT = "import_export"
PAGE_ROUNDS = "rounds"
PAGE_GAME = "game"
PAGE_QUESTION_LOG = "question_log"
PAGE_INSTRUCTOR_SETTINGS = "instructor_settings"
PAGE_ACCOUNT = "account"

PAGE_LABEL_KEYS = {
    PAGE_DASHBOARD: "nav.dashboard",
    PAGE_COURSES: "nav.courses",
    PAGE_STUDENTS: "nav.students",
    PAGE_LEARNING_UNITS: "nav.learning_units",
    PAGE_QUESTION_POOL: "nav.question_pool",
    PAGE_IMPORT_EXPORT: "nav.import_export",
    PAGE_ROUNDS: "nav.rounds",
    PAGE_GAME: "nav.game",
    PAGE_QUESTION_LOG: "nav.question_log",
    PAGE_INSTRUCTOR_SETTINGS: "nav.instructor_settings",
    PAGE_ACCOUNT: "nav.account",
}
PAGE_IDS = list(PAGE_LABEL_KEYS)

def persisted_locale():
    options = available_locales()
    saved = get_app_setting(conn, "ui_locale")
    if saved in options:
        return saved
    requested = initial_locale()
    return requested if requested in options else "en"


if "ui_locale" not in st.session_state:
    st.session_state.ui_locale = persisted_locale()


def tr(key, **params):
    return t(key, locale=st.session_state.get("ui_locale", "en"), **params)


def show_error(exc):
    if isinstance(exc, StorageError):
        st.error(tr(exc.code, **exc.params))
    else:
        st.error(str(exc))


def team_name(team):
    return tr("team.1") if int(team) == 1 else tr("team.2")


def player_mode_label(mode):
    return tr("game.player_mode.random") if mode == "random" else tr("game.player_mode.manual")


def undo_action_label(info):
    if not info:
        return ""
    return tr(info.get("action_key", "undo.action.score_card"), **(info.get("action_params") or {}))


def coverage_state_label(state):
    return {
        "open": tr("question_log.coverage.open"),
        "played": tr("question_log.coverage.played"),
        "running": tr("question_log.coverage.running"),
        "aborted": tr("question_log.coverage.aborted"),
    }.get(state, state)


def locale_selector(location, *, persist=False):
    current = st.session_state.get("ui_locale", "en")
    options = available_locales()
    if current not in options:
        current = "en"
        st.session_state.ui_locale = current
    selected = st.selectbox(
        tr("locale.selector"),
        options,
        index=options.index(current),
        format_func=locale_display_name,
        key=f"locale_selector_{location}",
    )
    if persist:
        st.caption(tr("locale.preference.caption"))
        if st.button(tr("locale.preference.save"), key=f"locale_save_{location}"):
            set_app_setting(conn, "ui_locale", selected)
            st.session_state.ui_locale = selected
            st.rerun()
    elif selected != current:
        st.session_state.ui_locale = selected
        st.rerun()


def rerun():
    st.rerun()


def login_screen():
    st.title(tr("app.title"))
    st.caption(f"{tr('app.tagline')} · {tr('app.version', version=APP_VERSION)}")
    locale_selector("login")
    st.caption(tr("app.name_origin"))
    if user_count(conn) == 0:
        st.subheader(tr("auth.setup.title"))
        st.info(tr("auth.setup.info"))
        with st.form("create_admin"):
            username=st.text_input(tr("auth.username"), value="instructor")
            password=st.text_input(tr("auth.password"), type="password")
            confirmation=st.text_input(tr("auth.password_repeat"), type="password")
            if st.form_submit_button(tr("auth.create_account"), type="primary"):
                ok,msg=create_admin(conn,username,password,confirmation)
                (st.success if ok else st.error)(tr(msg))
                if ok: st.rerun()
        return
    st.subheader(tr("auth.login.title"))
    with st.form("login"):
        username=st.text_input(tr("auth.username"))
        password=st.text_input(tr("auth.password"),type="password")
        if st.form_submit_button(tr("auth.login.submit"),type="primary"):
            ok,msg,display=authenticate(conn,username,password)
            if ok:
                st.session_state.authenticated=True
                st.session_state.username=display
                rerun()
            else:
                st.error(tr(msg))


if not st.session_state.get("authenticated"):
    login_screen()
    st.stop()

st.sidebar.title(tr("app.title"))
st.sidebar.caption(tr("app.tagline"))
PAGE=st.sidebar.radio(
    tr("nav.label"),
    PAGE_IDS,
    format_func=lambda page_id: tr(PAGE_LABEL_KEYS[page_id]),
    key="page_nav",
)
if st.sidebar.button(tr("auth.logout")):
    locale = persisted_locale()
    st.session_state.clear()
    st.session_state.ui_locale = locale
    rerun()


def navigate(page, game_id=None, clear_finished=False):
    st.session_state.page_nav=page
    if game_id is not None:
        st.session_state.active_game=game_id
    if clear_finished:
        st.session_state.pop("last_finished_game",None)


def clear_game_ui_state(game_id):
    for key in list(st.session_state.keys()):
        if str(key).startswith(f"assist_{game_id}_") or str(key).startswith(f"sub_") or str(key).startswith(f"next_{game_id}_"):
            st.session_state.pop(key,None)


def course_options():
    rows=list_courses(conn)
    return {f"{r['code']}{' – '+r['title'] if r['title'] else ''}":r["id"] for r in rows}


def question_options(active_only=True, learning_unit_id=None):
    rows=list_questions(conn,active_only)
    if learning_unit_id is not None:
        rows=[r for r in rows if r["learning_unit_id"]==learning_unit_id]
    return {f"F{r['id']:03d} · {r['unit_code']} · {r['question_text']}":r["id"] for r in rows}


def round_options():
    rows=list_rounds(conn)
    return {f"{r['name']} {'🔒' if r['locked'] else ''}":r["id"] for r in rows}


if PAGE==PAGE_DASHBOARD:
    st.title(tr("nav.dashboard"))
    rows=course_scoreboard(conn)
    if not rows:
        st.info(tr("dashboard.no_courses"))
    else:
        score_by_code={r["code"]:r for r in rows}
        selected_code=st.selectbox(tr("common.course"),list(score_by_code),key="dashboard_course")
        score=score_by_code[selected_code]

        m1,m2,m3,m4=st.columns(4,border=True)
        m1.metric(tr("dashboard.metric.team1_total"),int(score["team1_points"]))
        m2.metric(tr("dashboard.metric.team2_total"),int(score["team2_points"]))
        m3.metric(tr("dashboard.metric.rounds_played"),int(score["games_played"] or 0))
        diff=int(score["team1_points"])-int(score["team2_points"])
        leader=tr("dashboard.leader.tie") if diff==0 else (tr("team.1") if diff>0 else tr("team.2"))
        lead_value=leader if diff==0 else tr("dashboard.lead_value",leader=leader,points=abs(diff))
        m4.metric(tr("dashboard.metric.current_lead"),lead_value)

        running_course=[g for g in list_games(conn,"running") if g["course_id"]==score["id"]]
        if running_course:
            active=running_course[0]
            st.info(tr("dashboard.running_game",round_name=active["round_name"],course_code=active["course_code"]))
            st.button(
                tr("dashboard.resume_game"),
                type="primary",
                on_click=navigate,
                args=(PAGE_GAME,active["id"]),
                key=f"resume_dashboard_{active['id']}",
            )

        hist_course=[r for r in game_history(conn,score["id"]) if r["status"]=="finished"]
        hist_course=list(reversed(hist_course))

        round_col=tr("dashboard.column.round")
        team1_col=tr("team.1")
        team2_col=tr("team.2")
        if not hist_course:
            st.info(tr("dashboard.no_completed_round"))
        else:
            total1=total2=0
            trend=[]
            rounds_view=[]
            for r in hist_course:
                p1=int(r["team1_points"])
                p2=int(r["team2_points"])
                total1+=p1
                total2+=p2
                trend.append({round_col:r["round_name"],team1_col:total1,team2_col:total2})
                rounds_view.append({round_col:r["round_name"],team1_col:p1,team2_col:p2})

            if len(rounds_view)==1:
                last=rounds_view[0]
                st.subheader(tr("dashboard.previous_round"))
                st.info(tr(
                    "dashboard.single_round_score",
                    round_name=last[round_col],
                    team1=last[team1_col],
                    team2=last[team2_col],
                ))
            else:
                st.subheader(tr("dashboard.results_by_round"))
                rounds_df=pd.DataFrame(rounds_view)
                st.bar_chart(
                    rounds_df,
                    x=round_col,
                    y=[team1_col,team2_col],
                    x_label=None,
                    y_label=tr("dashboard.column.points"),
                    stack=False,
                    height=260,
                    use_container_width=True,
                )
                st.caption(tr("dashboard.caption.round_comparison"))

                st.subheader(tr("dashboard.total_progress"))
                trend_df=pd.DataFrame(trend)
                st.line_chart(
                    trend_df,
                    x=round_col,
                    y=[team1_col,team2_col],
                    x_label=None,
                    y_label=tr("dashboard.column.cumulative_points"),
                    height=260,
                    use_container_width=True,
                )
                st.caption(tr("dashboard.caption.cumulative"))

            with st.expander(tr("dashboard.round_results_table")):
                st.dataframe(pd.DataFrame(rounds_view),use_container_width=True,hide_index=True)

        with st.expander(tr("dashboard.all_courses")):
            df=pd.DataFrame([{
                tr("common.course"):r["code"],
                tr("team.1"):r["team1_points"],
                tr("team.2"):r["team2_points"],
                tr("dashboard.column.games"):r["games_played"],
                tr("dashboard.column.wins_t1"):r["team1_wins"],
                tr("dashboard.column.wins_t2"):r["team2_wins"],
                tr("dashboard.column.draws"):r["draws"],
            } for r in rows])
            st.dataframe(df,use_container_width=True,hide_index=True)

    with st.expander(tr("dashboard.game_history")):
        hist=game_history(conn)
        if hist:
            status_labels={"finished":tr("status.finished"),"running":tr("status.running"),"aborted":tr("status.aborted")}
            st.dataframe(pd.DataFrame([{
                tr("dashboard.column.round"):r["round_name"],
                tr("common.course"):r["course_code"],
                tr("dashboard.column.status"):status_labels.get(r["status"],r["status"]),
                tr("team.1"):r["team1_points"],
                tr("team.2"):r["team2_points"],
                tr("dashboard.column.start"):r["started_at"][:16].replace("T"," "),
            } for r in hist]),use_container_width=True,hide_index=True)
        else:
            st.caption(tr("dashboard.no_games"))

elif PAGE==PAGE_COURSES:
    st.title(tr("courses.title"))
    with st.form("new_course"):
        c1,c2=st.columns([1,2])
        code=c1.text_input(tr("courses.code"),placeholder=tr("courses.code.placeholder"))
        title=c2.text_input(tr("courses.name_optional"))
        if st.form_submit_button(tr("courses.create"),type="primary"):
            try:
                create_course(conn,code,title)
                st.success(tr("courses.created"))
                rerun()
            except StorageError as e:
                st.error(tr(e.code, **e.params))
            except Exception as e:
                show_error(e)
    rows=list_courses(conn,False)
    if rows:
        active_rows=[r for r in rows if r["active"]]
        archived_rows=[r for r in rows if not r["active"]]

        st.subheader(tr("courses.active.title"))
        if active_rows:
            st.dataframe(
                pd.DataFrame([{
                    tr("common.id"):r["id"],
                    tr("common.course"):r["code"],
                    tr("common.name"):r["title"],
                    tr("common.status"):tr("status.active"),
                } for r in active_rows]),
                hide_index=True,use_container_width=True,
            )
            archive_map={f"{r['code']}{' – '+r['title'] if r['title'] else ''}":r for r in active_rows}
            archive_label=st.selectbox(tr("courses.archive.select"),list(archive_map),key="archive_course_select")
            archive_row=archive_map[archive_label]
            st.caption(tr("courses.archive.caption"))
            if st.button(tr("courses.archive.button"),key="archive_course_button"):
                try:
                    archive_course(conn,archive_row["id"])
                    st.success(tr("courses.archive.success", code=archive_row["code"]))
                    rerun()
                except StorageError as e:
                    st.error(tr(e.code, **e.params))
                except Exception as e:
                    show_error(e)
        else:
            st.info(tr("courses.active.none"))

        with st.expander(tr("courses.archived.expander", count=len(archived_rows))):
            if archived_rows:
                st.dataframe(
                    pd.DataFrame([{
                        tr("common.id"):r["id"],
                        tr("common.course"):r["code"],
                        tr("common.name"):r["title"],
                        tr("common.status"):tr("status.archived"),
                    } for r in archived_rows]),
                    hide_index=True,use_container_width=True,
                )
                reactivate_map={f"{r['code']}{' – '+r['title'] if r['title'] else ''}":r for r in archived_rows}
                reactivate_label=st.selectbox(tr("courses.reactivate.select"),list(reactivate_map),key="reactivate_course_select")
                reactivate_row=reactivate_map[reactivate_label]
                if st.button(tr("courses.reactivate.button"),key="reactivate_course_button",type="primary"):
                    try:
                        reactivate_course(conn,reactivate_row["id"])
                        st.success(tr("courses.reactivate.success", code=reactivate_row["code"]))
                        rerun()
                    except StorageError as e:
                        st.error(tr(e.code, **e.params))
                    except Exception as e:
                        show_error(e)
            else:
                st.caption(tr("courses.archived.none"))

        st.divider()
        st.subheader(tr("courses.delete.title"))
        st.warning(tr("courses.delete.warning"))
        delete_map={
            f"{r['code']}{' – '+r['title'] if r['title'] else ''} · {tr('status.active') if r['active'] else tr('status.archived')}":r
            for r in rows
        }
        delete_label=st.selectbox(tr("courses.delete.select"),list(delete_map),key="delete_course_select")
        delete_row=delete_map[delete_label]
        n_students=len(list_students(conn,delete_row["id"],False))
        n_games=len(game_history(conn,delete_row["id"]))
        st.caption(tr("courses.delete.affected", students=n_students, games=n_games))
        confirm=st.text_input(tr("courses.delete.confirm", code=delete_row["code"]),key="delete_course_confirm")
        if st.button(tr("courses.delete.button"),disabled=confirm.strip().upper()!=delete_row["code"],type="secondary"):
            try:
                delete_course(conn,delete_row["id"])
                st.success(tr("courses.delete.success", code=delete_row["code"]))
                rerun()
            except StorageError as e:
                st.error(tr(e.code, **e.params))
            except Exception as e:
                show_error(e)

elif PAGE==PAGE_STUDENTS:
    st.title(tr("students.title"))
    opts=course_options()
    if not opts:
        st.warning(tr("students.no_course")); st.stop()
    label=st.selectbox(tr("common.course"),list(opts)); cid=opts[label]
    st.subheader(tr("students.csv.title"))
    uploaded=st.file_uploader(tr("students.csv.file"),type=["csv"],help=tr("students.csv.help"))
    if uploaded and st.button(tr("students.csv.import")):
        try:
            n,skip=import_students_csv(conn,cid,uploaded.getvalue())
            st.success(tr("students.csv.success", imported=n, skipped=skip)); rerun()
        except Exception as e: show_error(e)
    c1,c2=st.columns(2)
    with c1:
        with st.form("add_student"):
            name=st.text_input(tr("students.add_manual"))
            if st.form_submit_button(tr("students.add")):
                try: add_student(conn,cid,name); rerun()
                except Exception as e: show_error(e)
    with c2:
        st.write(tr("students.team_assignment"))
        if st.button(tr("students.randomize"),type="primary"):
            try: randomize_teams(conn,cid); st.success(tr("students.randomized")); rerun()
            except Exception as e: show_error(e)
    rows=list_students(conn,cid,False)
    if rows:
        st.subheader(tr("students.edit.title"))
        for student in rows:
            team_value=student["team"]
            team_display=team_name(team_value) if team_value in (1,2) else tr("students.team_unassigned")
            inactive=tr("students.inactive_suffix") if not student["active"] else ""
            with st.expander(tr("students.expander", name=student["display_name"], team=team_display, inactive=inactive)):
                with st.form(f"student_{student['id']}"):
                    name=st.text_input(tr("common.name"),value=student["display_name"])
                    team=st.selectbox(
                        tr("students.team"),
                        [None,1,2],
                        index={None:0,1:1,2:2}[student["team"]],
                        format_func=lambda value: tr("students.team_unassigned") if value is None else team_name(value),
                    )
                    active=st.checkbox(tr("students.active"),value=bool(student["active"]))
                    if st.form_submit_button(tr("students.save")):
                        try: update_student(conn,student["id"],name,team,active); rerun()
                        except Exception as e: show_error(e)
        t1=[student["display_name"] for student in rows if student["active"] and student["team"]==1]
        t2=[student["display_name"] for student in rows if student["active"] and student["team"]==2]
        a,b=st.columns(2)
        a.markdown(f"### {tr('team.1')}"); a.write("\n".join(f"- {x}" for x in t1) or "–")
        b.markdown(f"### {tr('team.2')}"); b.write("\n".join(f"- {x}" for x in t2) or "–")

elif PAGE==PAGE_LEARNING_UNITS:
    st.title(tr("learning_units.title"))
    st.caption(tr("learning_units.caption"))
    with st.form("new_unit"):
        a,b,c=st.columns([1,3,1])
        code=a.text_input(tr("learning_units.code"),placeholder=tr("learning_units.code.placeholder"))
        title=b.text_input(tr("learning_units.title_field"))
        pos=c.number_input(tr("learning_units.position"),min_value=0,step=1)
        if st.form_submit_button(tr("learning_units.create"),type="primary"):
            try: add_learning_unit(conn,code,title,pos); rerun()
            except Exception as e: show_error(e)
    rows=list_learning_units(conn,False)
    if not rows:
        st.info(tr("learning_units.none"))
    for unit in rows:
        qcount=learning_unit_question_count(conn,unit["id"])
        with st.expander(tr("learning_units.expander", code=unit["code"], title=unit["title"], position=unit["position"], count=qcount)):
            with st.form(f"uedit_{unit['id']}"):
                a,b,c=st.columns([1,3,1])
                edit_code=a.text_input(tr("learning_units.code"),value=unit["code"])
                edit_title=b.text_input(tr("learning_units.title_field"),value=unit["title"])
                edit_pos=c.number_input(tr("learning_units.position"),min_value=0,step=1,value=int(unit["position"]))
                save_col,delete_col=st.columns([2,1])
                save=save_col.form_submit_button(tr("learning_units.save"),type="primary",use_container_width=True)
                confirm_delete=st.checkbox(tr("learning_units.delete_confirm"),key=f"udel_confirm_{unit['id']}")
                delete=delete_col.form_submit_button(
                    tr("learning_units.delete"), disabled=(qcount>0 or not confirm_delete), use_container_width=True,
                )
                if qcount>0:
                    st.info(tr("learning_units.delete_blocked", count=qcount))
                if save:
                    try: update_learning_unit(conn,unit["id"],edit_code,edit_title,edit_pos); rerun()
                    except Exception as e: show_error(e)
                if delete:
                    try: delete_learning_unit(conn,unit["id"]); rerun()
                    except Exception as e: show_error(e)

elif PAGE==PAGE_QUESTION_POOL:
    st.title(tr("question_pool.title"))
    units=list_learning_units(conn)
    if not units:
        st.warning(tr("question_pool.no_units")); st.stop()
    umap={f"{u['code']} – {u['title']}":u["id"] for u in units}
    with st.form("new_question", clear_on_submit=True):
        unitlabel=st.selectbox(tr("question_pool.learning_unit"),list(umap))
        q=st.text_area(tr("question_pool.question"))
        a=st.text_area(tr("question_pool.answer_solution"))
        if st.form_submit_button(tr("question_pool.create"),type="primary"):
            try: add_question(conn,umap[unitlabel],q,a); rerun()
            except Exception as e: show_error(e)
    all_rows=list_questions(conn,False)
    unit_filter_labels={int(u["id"]):f"{u['code']} – {u['title']}" for u in units}
    selected_unit_id=st.selectbox(
        tr("question_pool.filter"), [None,*unit_filter_labels], key="question_pool_unit_filter",
        format_func=lambda unit_id: tr("question_pool.all_units") if unit_id is None else unit_filter_labels[unit_id],
    )
    rows=all_rows if selected_unit_id is None else [row for row in all_rows if row["learning_unit_id"]==selected_unit_id]
    if selected_unit_id is None:
        st.caption(tr("question_pool.count_all", count=len(rows)))
    else:
        st.caption(tr("question_pool.count_filtered", count=len(rows), total=len(all_rows)))
    for row in rows:
        with st.expander(f"F{row['id']:03d} · {row['unit_code']} · {row['question_text'][:90]}"):
            with st.form(f"qedit_{row['id']}"):
                ulabels=list(umap)
                current=next((i for i,x in enumerate(ulabels) if umap[x]==row["learning_unit_id"]),0)
                ul=st.selectbox(tr("question_pool.learning_unit"),ulabels,index=current)
                qt=st.text_area(tr("question_pool.question"),value=row["question_text"])
                at=st.text_area(tr("question_pool.answer"),value=row["answer_text"])
                active=st.checkbox(tr("question_pool.active"),value=bool(row["active"]))
                save_col,delete_col=st.columns([2,1])
                save=save_col.form_submit_button(tr("question_pool.save"),type="primary",use_container_width=True)
                confirm_delete=st.checkbox(tr("question_pool.delete_confirm"),key=f"qdel_confirm_{row['id']}")
                delete=delete_col.form_submit_button(tr("question_pool.delete"),disabled=not confirm_delete,use_container_width=True)
                if save:
                    try: update_question(conn,row["id"],umap[ul],qt,at,active); rerun()
                    except Exception as e: show_error(e)
                if delete:
                    try: delete_question(conn,row["id"]); rerun()
                    except Exception as e: show_error(e)

elif PAGE==PAGE_IMPORT_EXPORT:
    st.title(tr("import_export.title"))
    st.caption(tr("import_export.caption"))

    st.subheader(tr("import_export.export.title"))
    st.write(tr("import_export.export.info"))
    e1,e2=st.columns(2)
    e1.download_button(
        tr("import_export.export.json"), export_question_pool_json(conn),
        "Syzeteo-Question-Pool.json", "application/json", use_container_width=True,
    )
    e2.download_button(
        tr("import_export.export.csv"), export_question_pool_csv(conn),
        "Syzeteo-Question-Pool.csv", "text/csv", use_container_width=True,
    )

    st.divider()
    st.subheader(tr("import_export.import.title"))
    st.info(tr("import_export.import.info"))
    uploaded=st.file_uploader(tr("import_export.import.file"),type=["json"],key="question_pool_import")
    if uploaded is not None:
        raw=uploaded.getvalue()
        try:
            preview=preview_question_pool_import(conn,raw)
            st.success(tr("import_export.import.preview_ok"))
            a,b,c,d=st.columns(4,border=True)
            a.metric(tr("import_export.metric.units_total"),preview["learning_units_total"])
            b.metric(tr("import_export.metric.units_new"),preview["new_units"])
            c.metric(tr("import_export.metric.questions_total"),preview["questions_total"])
            d.metric(tr("import_export.metric.questions_new"),preview["new_questions"])
            st.caption(tr("import_export.preview.summary", reused=preview["reused_units"], duplicates=preview["duplicate_questions"]))
            if preview["unit_conflicts"]:
                st.warning(tr("import_export.unit_conflicts"))
                conflict_df=pd.DataFrame(preview["unit_conflicts"]).rename(columns={
                    "code":tr("import_export.conflict.code"),
                    "existing_title":tr("import_export.conflict.existing_title"),
                    "import_title":tr("import_export.conflict.import_title"),
                    "existing_position":tr("import_export.conflict.existing_position"),
                    "import_position":tr("import_export.conflict.import_position"),
                })
                st.dataframe(conflict_df,use_container_width=True,hide_index=True)
            confirm=st.checkbox(tr("import_export.confirm"),key="confirm_question_pool_import")
            if st.button(tr("import_export.start"),type="primary",disabled=not confirm,use_container_width=True):
                result=import_question_pool_json(conn,raw)
                st.success(tr("import_export.success", units=result["added_units"], questions=result["added_questions"], skipped=result["skipped_questions"]))
        except Exception as e:
            show_error(e)

elif PAGE==PAGE_ROUNDS:
    st.title(tr("rounds.title"))
    qopts=question_options(True)
    units=list_learning_units(conn)
    unit_filter_labels={int(u["id"]):f"{u['code']} – {u['title']}" for u in units}
    if len(qopts)<8:
        st.warning(tr("rounds.need_eight"))

    new_round_unit_id=st.selectbox(
        tr("rounds.filter_new"), [None,*unit_filter_labels], key="new_round_unit_filter",
        format_func=lambda unit_id: tr("rounds.all_units") if unit_id is None else unit_filter_labels[unit_id],
    )
    new_round_qopts=question_options(True,new_round_unit_id) if new_round_unit_id is not None else qopts
    st.caption(tr("rounds.active_count", count=len(new_round_qopts)))
    with st.form("new_round"):
        name=st.text_input(tr("rounds.name"),placeholder=tr("rounds.name.placeholder"))
        selected=st.multiselect(tr("rounds.select_eight"),list(new_round_qopts),max_selections=8)
        if st.form_submit_button(tr("rounds.create"),type="primary"):
            try: create_round(conn,name,[new_round_qopts[x] for x in selected]); st.success(tr("rounds.created")); rerun()
            except Exception as e: show_error(e)
    for rnd in list_rounds(conn):
        state=tr("rounds.state.locked") if rnd["locked"] else tr("rounds.state.editable")
        with st.expander(tr("rounds.expander", name=rnd["name"], count=rnd["n_questions"], state=state)):
            rq=round_questions(conn,rnd["id"])
            for item in rq:
                st.write(f"{item['position']}. **{item['unit_code']}** – {item['question_text']}")
            st.write(tr("rounds.challenge_auto"))
            if not rnd["locked"] and len(qopts)>=8:
                selected_labels=[]
                ids={item["question_id"] for item in rq}
                for label,qid in qopts.items():
                    if qid in ids: selected_labels.append(label)
                edit_unit_id=st.selectbox(
                    tr("rounds.filter_edit"), [None,*unit_filter_labels], key=f"edit_round_unit_filter_{rnd['id']}",
                    format_func=lambda unit_id: tr("rounds.all_units") if unit_id is None else unit_filter_labels[unit_id],
                )
                filtered_qopts=question_options(True,edit_unit_id) if edit_unit_id is not None else qopts
                edit_qopts=dict(filtered_qopts)
                for label in selected_labels:
                    if label in qopts:
                        edit_qopts[label]=qopts[label]
                with st.form(f"edit_round_{rnd['id']}"):
                    newsel=st.multiselect(tr("rounds.change_questions"),list(edit_qopts),default=selected_labels,max_selections=8)
                    if st.form_submit_button(tr("rounds.save")):
                        try: update_round_questions(conn,rnd["id"],[edit_qopts[x] for x in newsel]); rerun()
                        except Exception as e: show_error(e)
            else:
                st.info(tr("rounds.locked_info"))

elif PAGE==PAGE_GAME:
    st.title(tr("game.title"))

    # Nach der letzten Karte bleibt ein klarer Abschlussbildschirm stehen.
    finished_id=st.session_state.get("last_finished_game")
    if finished_id:
        finished_game=get_game(conn,finished_id)
        if finished_game and finished_game["status"]=="finished":
            st.subheader(tr("game.finished.title", round_name=finished_game["round_name"], course_code=finished_game["course_code"]))
            a,b,c=st.columns([1,0.65,1],vertical_alignment="center")
            a.metric(tr("team.1"),int(finished_game["team1_points"]))
            b.markdown("<div style='text-align:center;font-size:2rem;font-weight:700'>:</div>",unsafe_allow_html=True)
            c.metric(tr("team.2"),int(finished_game["team2_points"]))
            p1=int(finished_game["team1_points"]); p2=int(finished_game["team2_points"])
            if p1==p2:
                st.info(tr("game.finished.draw"))
            else:
                winner=1 if p1>p2 else 2
                st.success(tr("game.finished.winner", team=winner, high=max(p1,p2), low=min(p1,p2)))
            score=next((r for r in course_scoreboard(conn) if r["id"]==finished_game["course_id"]),None)
            if score:
                st.markdown(tr("game.finished.course_total"))
                g1,g2=st.columns(2,border=True)
                g1.metric(tr("dashboard.metric.team1_total"),int(score["team1_points"]))
                g2.metric(tr("dashboard.metric.team2_total"),int(score["team2_points"]))
            st.caption(tr("game.privacy"))
            u=undo_info(conn,finished_id)
            x,y,z=st.columns(3)
            if u:
                if x.button(tr("game.undo"),key=f"undo_finish_{finished_id}"):
                    try:
                        undo_last_action(conn,finished_id)
                        clear_game_ui_state(finished_id)
                        st.session_state.pop("last_finished_game",None)
                        st.session_state.active_game=finished_id
                        rerun()
                    except Exception as e:
                        show_error(e)
            y.button(tr("game.dashboard"),type="primary",on_click=navigate,args=(PAGE_DASHBOARD,None,True),key=f"dash_finish_{finished_id}")
            z.button(tr("game.next_game"),on_click=navigate,args=(PAGE_GAME,None,True),key=f"next_finish_{finished_id}")
            st.stop()
        else:
            st.session_state.pop("last_finished_game",None)

    running=list_games(conn,"running")
    running_ids={g["id"] for g in running}
    active_gid=st.session_state.get("active_game")
    if active_gid not in running_ids:
        active_gid=None
        st.session_state.pop("active_game",None)
    if running:
        labels={tr("game.running.label", round_name=g["round_name"], course_code=g["course_code"]):g["id"] for g in running}
        if active_gid is not None:
            chosen_label=next((label for label,gid0 in labels.items() if gid0==active_gid),next(iter(labels)))
            chosen=st.selectbox(tr("game.running.open"),list(labels),index=list(labels).index(chosen_label),key="running_game_select")
        else:
            chosen=st.selectbox(tr("game.running.open"),list(labels),key="running_game_select")
        gid=labels[chosen]
        st.session_state.active_game=gid
    else:
        gid=None
    st.divider()

    if gid is None:
        st.subheader(tr("game.prepare"))
        copts=course_options(); ropts=round_options()
        if not copts or not ropts:
            st.warning(tr("common.course_and_round_required")); st.stop()
        cl=st.selectbox(tr("common.course"),list(copts)); rl=st.selectbox(tr("common.round"),list(ropts)); cid=copts[cl]; rid=ropts[rl]
        already={g["round_id"] for g in game_history(conn,cid)}
        questions_ok=len(round_questions(conn,rid))==8
        students=[s for s in list_students(conn,cid,True) if s["team"] in (1,2)]
        team1=[s for s in students if s["team"]==1]
        team2=[s for s in students if s["team"]==2]
        st.markdown(tr("game.attendance.title"))
        st.caption(tr("game.attendance.caption"))
        # Die beiden Anwesenheitsfelder zeigen auch größere Teams möglichst ohne internes Scrollen.
        st.markdown(
            """
            <style>
            /* Anwesenheitscheck: bis zu ca. 15 Namen ohne internes Scrollen sichtbar. */
            div[class*="st-key-present1_"] [data-baseweb="select"],
            div[class*="st-key-present2_"] [data-baseweb="select"] {
                min-height: 320px !important;
                height: auto !important;
            }
            div[class*="st-key-present1_"] [data-baseweb="select"] > div,
            div[class*="st-key-present2_"] [data-baseweb="select"] > div {
                min-height: 320px !important;
                height: auto !important;
                align-items: flex-start !important;
                align-content: flex-start !important;
            }
            div[class*="st-key-present1_"] [data-baseweb="select"] > div > div,
            div[class*="st-key-present2_"] [data-baseweb="select"] > div > div {
                max-height: none !important;
                height: auto !important;
                overflow-y: visible !important;
                align-content: flex-start !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        t1map={s["display_name"]:s["id"] for s in team1}
        t2map={s["display_name"]:s["id"] for s in team2}
        c1,c2=st.columns(2)
        present1=c1.multiselect(tr("game.attendance.team", team=1),list(t1map),default=list(t1map),key=f"present1_{cid}_{rid}")
        present2=c2.multiselect(tr("game.attendance.team", team=2),list(t2map),default=list(t2map),key=f"present2_{cid}_{rid}")
        present_ids=[t1map[x] for x in present1]+[t2map[x] for x in present2]

        st.markdown(tr("game.starter.title"))
        starter_mode=st.radio(
            tr("game.starter.mode"),
            ["random", "manual"],
            format_func=lambda value: tr("common.random") if value=="random" else tr("common.manual"),
            horizontal=True,
            index=0,
            key=f"starter_mode_{cid}_{rid}",
            help=tr("game.starter.help"),
        )
        starter_id=None
        if starter_mode=="manual":
            present_id_set={int(x) for x in present_ids}
            present_roster=[s for s in students if int(s["id"]) in present_id_set]
            starter_map={
                f"{s['display_name']} · Team {s['team']}":s["id"]
                for s in present_roster
            }
            starter_label=st.selectbox(
                tr("game.starter.select"),
                list(starter_map),
                index=None,
                placeholder=tr("game.starter.placeholder"),
                key=f"starter_manual_{cid}_{rid}",
            )
            starter_id=starter_map.get(starter_label) if starter_label else None
        regular_mode=st.session_state.get(f"next_player_mode_{cid}","random")
        regular_mode_label=player_mode_label(regular_mode)
        st.caption(tr("game.player_mode.next_caption", mode=regular_mode_label))

        st.markdown(tr("game.precheck.title"))
        already_ok=rid not in already
        team1_ok=len(present1)>=4
        team2_ok=len(present2)>=4
        checks=[
            (questions_ok,tr("game.precheck.questions", count=len(round_questions(conn,rid)))),
            (already_ok,tr("game.precheck.round_new") if already_ok else tr("game.precheck.round_used")),
            (team1_ok,tr("game.precheck.team", team=1, count=len(present1))),
            (team2_ok,tr("game.precheck.team", team=2, count=len(present2))),
        ]
        for ok,text in checks:
            st.write(f"{'✓' if ok else '✗'} {text}")
        if starter_mode=="manual":
            starter_ok=starter_id is not None
            checks.append((starter_ok,tr("game.precheck.starter_ok") if starter_ok else tr("game.precheck.starter_missing")))
            ok,text=checks[-1]
            st.write(f"{'✓' if ok else '✗'} {text}")
        ready=all(ok for ok,_ in checks)
        if not ready:
            st.warning(tr("game.precheck.not_ready"))
        if st.button(tr("game.start"),type="primary",disabled=not ready):
            try:
                gid=start_game(conn,rid,cid,present_ids,starter_mode,starter_id,regular_mode)
                # The setting applies to the started game only; the next game returns
                # to the required default random player selection.
                st.session_state[f"next_player_mode_{cid}"]="random"
                st.session_state.pop(f"player_mode_control_{cid}",None)
                st.session_state.active_game=gid
                rerun()
            except Exception as e:
                show_error(e)

    if gid:
        game=get_game(conn,gid); cards=game_cards(conn,gid); player=current_player(conn,game)
        top1,top2=st.columns([3,1],vertical_alignment="center")
        top1.subheader(f"{game['round_name']} · {game['course_code']}")
        presentation=top2.toggle(tr("game.presentation"),key=f"presentation_{gid}",help=tr("game.presentation.help"))
        if presentation:
            st.markdown("""
            <style>
            [data-testid="stSidebar"] {display:none !important;}
            [data-testid="stHeader"] {height:0 !important; min-height:0 !important;}
            [data-testid="stToolbar"], #MainMenu, footer {display:none !important;}
            .block-container {padding-top:0.5rem !important; padding-bottom:0.7rem !important; max-width:none !important;}
            </style>
            """,unsafe_allow_html=True)

        s1,s2,s3=st.columns([1,1,1])
        s1.metric(tr("team.1"),game["team1_points"])
        s2.metric(tr("team.2"),game["team2_points"])
        u=undo_info(conn,gid)
        if u:
            if s3.button(tr("game.undo"),key=f"undo_{gid}",help=tr("game.undo.help", action=undo_action_label(u))):
                try:
                    undo_last_action(conn,gid)
                    clear_game_ui_state(gid)
                    st.session_state.pop("last_finished_game",None)
                    rerun()
                except Exception as e:
                    show_error(e)
        j1,j2=st.columns(2)
        j1.caption(tr("game.assist.status", team=1, status=tr("common.used") if game["team1_assist_used"] else tr("common.available")))
        j2.caption(tr("game.assist.status", team=2, status=tr("common.used") if game["team2_assist_used"] else tr("common.available")))
        regular_mode_label=player_mode_label(game["player_selection_mode"])
        abort_confirm_key=f"abort_confirm_{gid}"
        if st.button(tr("game.abort.button"),key=f"abort_game_{gid}",type="secondary"):
            st.session_state[abort_confirm_key]=True
            rerun()
        if st.session_state.get(abort_confirm_key):
            st.warning(tr("game.abort.warning",round_name=game["round_name"],course_code=game["course_code"]))
            abort_yes,abort_no=st.columns(2)
            if abort_yes.button(tr("game.abort.confirm"),key=f"abort_game_confirm_{gid}",type="primary"):
                try:
                    aborted_round=game["round_name"]
                    aborted_course=game["course_code"]
                    abort_game(conn,gid)
                    clear_game_ui_state(gid)
                    st.session_state.pop("active_game",None)
                    st.session_state.pop(abort_confirm_key,None)
                    st.session_state["game_abort_success"]={"round_name":aborted_round,"course_code":aborted_course}
                    st.session_state.page_nav=PAGE_INSTRUCTOR_SETTINGS
                    rerun()
                except Exception as e:
                    show_error(e)
            if abort_no.button(tr("game.abort.cancel"),key=f"abort_game_cancel_{gid}"):
                st.session_state.pop(abort_confirm_key,None)
                rerun()

        st.caption(tr("game.player_mode.running", mode=regular_mode_label))

        # US #3: Abwesende aktive Studierende können während der laufenden Runde nachgetragen werden.
        if game["status"]=="running":
            roster_ids={int(r["student_id"]) for r in game_roster(conn,gid)}
            late_students=[
                s for s in list_students(conn,game["course_id"],True)
                if s["team"] in (1,2) and int(s["id"]) not in roster_ids
            ]
            with st.expander(tr("game.late.title")):
                if late_students:
                    late_map={f"{s['display_name']} · Team {s['team']}":s["id"] for s in late_students}
                    late_label=st.selectbox(
                        tr("game.late.person"), list(late_map), index=None,
                        placeholder=tr("game.person.select"), key=f"late_player_{gid}"
                    )
                    if st.button(tr("game.late.add"),disabled=late_label is None,key=f"late_add_{gid}"):
                        try:
                            add_late_player(conn,gid,late_map[late_label]); rerun()
                        except Exception as e:
                            show_error(e)
                else:
                    st.caption(tr("game.late.none"))

        # Änderungen an Startspieler/Nachzüglern können den aktuellen Spieler verändert haben.
        game=get_game(conn,gid); cards=game_cards(conn,gid); player=current_player(conn,game)
        unresolved=[c for c in cards if not c["resolved"]]
        open_cards=[c for c in unresolved if c["revealed"]]
        resolved_count=sum(1 for c in cards if c["resolved"])
        instructor_turn=len(unresolved)==1
        awaiting_next_player=(
            game["status"]=="running"
            and len(unresolved)>1
            and not open_cards
            and resolved_count >= int(game["turn_no"])
        )
        if instructor_turn:
            st.info(tr("game.last_card.info"))
        elif player:
            st.markdown(tr("game.current_player", name=player["display_name_snapshot"], team=player["team_snapshot"]))
        st.markdown(tr("game.board"))
        # Alle neun Kacheln erhalten dieselbe Höhe. Die Höhe wird konservativ aus
        # dem längsten Fragetext der Runde abgeleitet, damit kein Text überläuft.
        max_card_lines=3
        for c in cards:
            if c["card_type"]==CARD_TYPE_CHALLENGE:
                estimated_lines=2
            else:
                question=c["question_text_snapshot"] or ""
                wrapped=textwrap.wrap(
                    question,
                    width=34,
                    break_long_words=True,
                    break_on_hyphens=True,
                ) or [""]
                estimated_lines=1+len(wrapped)
            max_card_lines=max(max_card_lines,estimated_lines)
        card_height=max(112,72+max_card_lines*27)
        card_css="""
        <style>
        [class*="st-key-syzeteo_card_"] button {
            min-height: __CARD_HEIGHT__px;
            height: __CARD_HEIGHT__px;
            border-radius: 12px;
            border: 2px solid rgba(49, 51, 63, 0.24);
            box-shadow: 0 4px 11px rgba(0, 0, 0, 0.15);
            padding: 10px 14px;
            white-space: normal !important;
            overflow: visible !important;
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        [class*="st-key-syzeteo_card_"] button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.20);
        }
        [class*="st-key-syzeteo_card_"] button p {
            white-space: normal !important;
            overflow: visible !important;
            overflow-wrap: anywhere;
            word-break: break-word;
            line-height: 1.20;
            font-size: 1.16rem;
            margin: 0;
        }
        [class*="st-key-syzeteo_card_back_"] button {
            background: linear-gradient(145deg, #30343b, #17191d);
            color: white;
            border-color: #555b66;
        }
        [class*="st-key-syzeteo_card_back_"] button p {
            font-size: 1.24rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }
        [class*="st-key-syzeteo_card_face_"] button {
            background: #fffdf8;
            color: #1f2328;
            border-color: #c8c0b2;
        }
        [class*="st-key-syzeteo_card_done_"] button {
            background: #f4f2ed;
            color: #555;
            border-color: #d4d0c8;
            opacity: 0.82;
        }
        </style>
        """.replace("__CARD_HEIGHT__",str(card_height))
        st.markdown(card_css,unsafe_allow_html=True)
        for row in range(3):
            cols=st.columns(3)
            for col in range(3):
                card=cards[row*3+col]
                if not card["revealed"]:
                    state="back"
                    label=tr("game.card.back", card_no=card["card_no"])
                elif card["card_type"]==CARD_TYPE_CHALLENGE:
                    state="done" if card["resolved"] else "face"
                    prefix="✓ " if card["resolved"] else ""
                    label=f"{prefix}**Challenge Card**\n\nKnowledge. Teams. Rounds."
                else:
                    state="done" if card["resolved"] else "face"
                    prefix="✓ " if card["resolved"] else ""
                    unit=card["unit_code_snapshot"] or ""
                    question=card["question_text_snapshot"] or ""
                    label=f"{prefix}**{unit}**\n\n{question}"
                with cols[col].container(key=f"syzeteo_card_{state}_{card['id']}"):
                    if st.button(label,key=f"card_{gid}_{card['id']}",use_container_width=True,disabled=bool(open_cards and not card["revealed"]) or bool(awaiting_next_player and not card["revealed"]) or card["resolved"]):
                        try:
                            reveal_card(conn,gid,card["card_no"]); rerun()
                        except Exception as e:
                            show_error(e)
        cards=game_cards(conn,gid); current=next((c for c in cards if c["revealed"] and not c["resolved"]),None)
        if current:
            st.divider()
            if instructor_turn:
                if current["card_type"]=="question":
                    st.markdown(f"### {current['unit_code_snapshot']} · {tr('game.instructor_turn')}")
                    st.write(current["question_text_snapshot"])
                    with st.expander(tr("game.model_answer")): st.write(current["answer_text_snapshot"] or "–")
                else:
                    st.markdown(f"### {tr('game.challenge.title')}")
                    st.write(tr("game.last_challenge"))
                if st.button(tr("game.last_card.finish"),type="primary"):
                    try:
                        resolve_instructor_card(conn,gid,current["id"])
                        st.session_state.last_finished_game=gid
                        st.session_state.pop("active_game",None)
                        rerun()
                    except Exception as e:
                        show_error(e)
            elif current["card_type"]==CARD_TYPE_CHALLENGE:
                st.markdown(f"## {tr('game.challenge.title')}")
                st.write(tr("game.challenge.prompt"))
                st.write(tr("game.challenge.scoring"))
                a,b,c=st.columns(3)
                if a.button(tr("game.challenge.no_answer"),type="primary"):
                    resolve_question(conn,gid,current["id"],2); rerun()
                if b.button(tr("game.challenge.answered")):
                    resolve_question(conn,gid,current["id"],1); rerun()
                if c.button(tr("game.challenge.not_relevant")):
                    resolve_question(conn,gid,current["id"],0); rerun()
            else:
                st.markdown(f"## {current['unit_code_snapshot']}")
                st.write(current["question_text_snapshot"])
                components.html(f"""
                    <div style='font-family:sans-serif;font-size:22px'>{tr("game.timer_label")} <strong id='t'>60</strong> s</div>
                    <script>let n=60; const e=document.getElementById('t'); const x=setInterval(()=>{{n--;e.textContent=Math.max(n,0);if(n<=0)clearInterval(x)}},1000);</script>
                """,height=45)
                with st.expander(tr("game.model_answer")): st.write(current["answer_text_snapshot"] or "–")
                a,b,c=st.columns(3)
                if a.button(tr("game.correct"),type="primary"):
                    resolve_question(conn,gid,current["id"],1); rerun()
                if b.button(tr("game.wrong")):
                    resolve_question(conn,gid,current["id"],0); rerun()
                game=get_game(conn,gid); team=game["current_team"]
                assist_used=game["team1_assist_used"] if team==1 else game["team2_assist_used"]
                if c.button(tr("game.assist.use"),disabled=bool(assist_used)):
                    st.session_state[f"assist_{gid}_{current['id']}"]=True; rerun()
                if st.session_state.get(f"assist_{gid}_{current['id']}"):
                    mates=[r for r in game_roster(conn,gid,team) if r["student_id"]!=game["current_student_id"]]
                    mmap={m["display_name_snapshot"]:m["student_id"] for m in mates}
                    if not mmap:
                        st.warning(tr("game.assist.no_mate"))
                    else:
                        substitute=st.selectbox(tr("game.assist.who"),list(mmap),key=f"sub_{current['id']}")
                        x,y=st.columns(2)
                        if x.button(tr("game.assist.correct"),key=f"ar_{current['id']}"):
                            resolve_question(conn,gid,current["id"],1,True,mmap[substitute]); st.session_state.pop(f"assist_{gid}_{current['id']}",None); rerun()
                        if y.button(tr("game.assist.wrong"),key=f"af_{current['id']}"):
                            resolve_question(conn,gid,current["id"],0,True,mmap[substitute]); st.session_state.pop(f"assist_{gid}_{current['id']}",None); rerun()

        # Ab Spieler 2 hängt die Auswahl vom vor Spielbeginn eingefrorenen Modus ab.
        game=get_game(conn,gid); all_cards=game_cards(conn,gid); unresolved=[c for c in all_cards if not c["resolved"]]
        no_open=not any(c["revealed"] and not c["resolved"] for c in all_cards)
        resolved_count=sum(1 for c in all_cards if c["resolved"])
        awaiting_next=(
            game["status"]=="running" and len(unresolved)>1 and no_open
            and resolved_count >= int(game["turn_no"])
        )
        if awaiting_next:
            next_team=2 if game["current_team"]==1 else 1
            candidates=[r for r in game_roster(conn,gid,next_team) if not r["has_played"]]
            st.divider()
            if game["player_selection_mode"]=="manual":
                st.markdown(tr("game.next.manual.title", team=next_team))
                if not candidates:
                    st.error(tr("game.next.no_candidate", team=next_team))
                else:
                    cmap={r["display_name_snapshot"]:r["student_id"] for r in candidates}
                    chosen=st.selectbox(
                        tr("game.next.player", team=next_team),list(cmap),index=None,
                        placeholder=tr("game.person.select"),key=f"next_manual_{gid}_{game['turn_no']}"
                    )
                    if st.button(
                        tr("game.next.accept"),type="primary",disabled=chosen is None,
                        key=f"next_manual_btn_{gid}_{game['turn_no']}"
                    ):
                        try:
                            set_next_player(conn,gid,cmap[chosen]); rerun()
                        except Exception as e:
                            show_error(e)
            else:
                st.markdown(tr("game.next.random.title", team=next_team))
                if not candidates:
                    st.error(tr("game.next.no_candidate", team=next_team))
                else:
                    st.warning(tr("game.next.random_failed"))

elif PAGE==PAGE_QUESTION_LOG:
    st.title(tr("question_log.title"))
    st.caption(tr("question_log.caption"))
    rows=protocol_rows(conn)
    if rows:
        col_round=tr("question_log.col.round")
        col_position=tr("question_log.col.position")
        col_qid=tr("question_log.col.question_id")
        col_unit=tr("question_log.col.unit")
        col_question=tr("question_log.col.question")
        col_course=tr("question_log.col.course")
        col_status=tr("question_log.col.status")
        col_played=tr("question_log.col.played_on")
        data=[]
        for row in rows:
            data.append({
                col_round:row["round_name"], col_position:row["position"], col_qid:f"F{row['question_id']:03d}",
                col_unit:row["unit_code"], col_question:row["question_text"], col_course:row["course_code"],
                col_status:{"finished":tr("status.finished"),"running":tr("status.running"),"aborted":tr("status.aborted")}.get(row["status"],row["status"]), col_played:((row["resolved_at"] or row["started_at"] or "")[:10]),
            })
        df=pd.DataFrame(data)
        courses=sorted(df[col_course].unique())
        c1,c2=st.columns(2)
        course_filter=c1.multiselect(tr("question_log.filter.course"),courses)
        rounds=sorted(df[col_round].unique())
        round_filter=c2.multiselect(tr("question_log.filter.round"),rounds)
        view=df.copy()
        if course_filter: view=view[view[col_course].isin(course_filter)]
        if round_filter: view=view[view[col_round].isin(round_filter)]
        st.dataframe(view,use_container_width=True,hide_index=True)
        st.download_button(tr("question_log.export"),view.to_csv(index=False).encode("utf-8-sig"),"Syzeteo-Question-Log.csv","text/csv")
    else:
        st.info(tr("question_log.none"))

    st.subheader(tr("question_log.coverage.title"))
    all_courses=list_courses(conn)
    all_rounds=list(reversed(list_rounds(conn)))
    all_games=list_games(conn)
    if not all_courses or not all_rounds:
        st.caption(tr("question_log.coverage.need_data"))
    else:
        round_col=tr("question_log.col.round")
        coverage_col=tr("question_log.coverage.col")
        coverage=[]
        for rnd in all_rounds:
            row={round_col:rnd["name"]}
            finished_all=True
            for course in all_courses:
                game=next((g for g in all_games if g["round_id"]==rnd["id"] and g["course_id"]==course["id"]),None)
                if game and game["status"]=="finished":
                    status=tr("question_log.coverage.played")
                elif game and game["status"]=="running":
                    status=tr("question_log.coverage.running"); finished_all=False
                elif game and game["status"]=="aborted":
                    status=tr("question_log.coverage.aborted"); finished_all=False
                else:
                    status=tr("question_log.coverage.open"); finished_all=False
                row[course["code"]]=status
            row[coverage_col]=tr("question_log.coverage.complete") if finished_all else tr("question_log.coverage.incomplete")
            coverage.append(row)
        st.dataframe(pd.DataFrame(coverage),use_container_width=True,hide_index=True)
        complete=sum(1 for row in coverage if row[coverage_col]==tr("question_log.coverage.complete"))
        st.caption(tr("question_log.coverage.summary", complete=complete, total=len(coverage)))

elif PAGE==PAGE_INSTRUCTOR_SETTINGS:
    st.title(tr("settings.title"))
    aborted_flash=st.session_state.pop("game_abort_success",None)
    if aborted_flash:
        st.success(tr("game.abort.success",**aborted_flash))
    deleted_flash=st.session_state.pop("game_delete_success",None)
    if deleted_flash:
        st.success(tr("settings.aborted.deleted",**deleted_flash))

    st.caption(tr("settings.caption"))

    st.subheader(tr("locale.selector"))
    locale_selector("instructor_settings", persist=True)

    st.subheader(tr("settings.system.title"))
    system=dashboard_system_status(conn)
    a,b,c,d=st.columns(4,border=True)
    a.metric(tr("settings.metric.version"),APP_VERSION)
    b.metric(tr("settings.metric.database"),"OK" if system["database_ok"] else tr("settings.database.error"))
    c.metric(tr("settings.metric.courses"),system["courses"])
    d.metric(tr("settings.metric.students"),system["students"])
    a,b,c,d=st.columns(4,border=True)
    a.metric(tr("settings.metric.units"),system["learning_units"])
    b.metric(tr("settings.metric.active_questions"),system["questions_active"])
    c.metric(tr("settings.metric.rounds"),system["rounds"])
    d.metric(tr("settings.metric.running_games"),system["running_games"])
    st.caption(tr("settings.archived_questions", count=system["questions_archived"]))

    issues=dashboard_configuration_issues(conn)
    if not issues:
        st.success(tr("settings.config.ok"))
    else:
        problem_count=sum(1 for issue in issues if issue["level"] in ("warning","error"))
        if problem_count:
            st.warning(tr("settings.config.problems", count=problem_count))
        else:
            st.info(tr("settings.config.info_only"))
        for idx,issue in enumerate(issues):
            renderer={"error":st.error,"warning":st.warning,"info":st.info}.get(issue["level"],st.info)
            title=tr(issue["title_key"], **issue.get("title_params",{}))
            impact=tr(issue["impact_key"], **issue.get("impact_params",{}))
            solution=tr(issue["solution_key"], **issue.get("solution_params",{}))
            renderer(f"**{title}**\n\n{impact}\n\n{tr('settings.config.solution', solution=solution)}")
            if issue.get("action_page") and issue.get("action_key"):
                st.button(tr(issue["action_key"]),key=f"config_issue_action_{idx}",on_click=navigate,args=(issue["action_page"],))

    st.divider()
    st.subheader(tr("settings.courses_students.title"))
    courses=list_courses(conn)
    selected_course_id=None
    course_status=None
    if not courses:
        st.info(tr("settings.no_courses"))
        st.button(tr("settings.manage_courses"),key="admin_courses_empty",on_click=navigate,args=(PAGE_COURSES,))
    else:
        course_labels={f"{row['code']}{' – '+row['title'] if row['title'] else ''}":int(row["id"]) for row in courses}
        valid_ids=set(course_labels.values())
        remembered=st.session_state.get("instructor_course_id")
        if remembered not in valid_ids:
            remembered=next(iter(valid_ids)); st.session_state.instructor_course_id=remembered
        current_label=next(label for label,cid0 in course_labels.items() if cid0==remembered)
        selected_label=st.selectbox(tr("settings.course"),list(course_labels),index=list(course_labels).index(current_label),key="instructor_course_select")
        selected_course_id=course_labels[selected_label]
        st.session_state.instructor_course_id=selected_course_id
        course_status=dashboard_course_status(conn,selected_course_id)

        c1,c2,c3,c4=st.columns(4,border=True)
        c1.metric(tr("settings.metric.students"),course_status["students"])
        c2.metric(tr("team.1"),course_status["team1"])
        c3.metric(tr("team.2"),course_status["team2"])
        c4.metric(tr("settings.metric.unassigned"),course_status["unassigned"])
        if course_status["students"]==0:
            st.warning(tr("settings.course.no_students", code=course_status["code"]))
        elif course_status["unassigned"]:
            st.warning(tr("settings.course.unassigned", count=course_status["unassigned"]))
        else:
            st.success(tr("settings.course.ok"))
        b1,b2,b3=st.columns(3)
        b1.button(tr("settings.manage_courses"),use_container_width=True,key="admin_courses",on_click=navigate,args=(PAGE_COURSES,))
        b2.button(tr("settings.manage_students"),use_container_width=True,key="admin_students",on_click=navigate,args=(PAGE_STUDENTS,))
        b3.button(tr("settings.prepare_game"),use_container_width=True,key="admin_attendance",on_click=navigate,args=(PAGE_GAME,))

    st.divider()
    st.subheader(tr("settings.content.title"))
    unit_rows=dashboard_learning_unit_status(conn)
    active_units=[unit for unit in unit_rows if unit["active"]]
    a,b,c=st.columns(3,border=True)
    a.metric(tr("settings.metric.active_units"),len(active_units))
    b.metric(tr("settings.metric.active_questions"),system["questions_active"])
    c.metric(tr("settings.metric.archived_questions"),system["questions_archived"])
    if active_units:
        unit_df=pd.DataFrame([{
            tr("settings.table.unit"):unit["code"],
            tr("settings.table.name"):unit["title"],
            tr("settings.metric.active_questions"):int(unit["active_questions"] or 0),
            tr("settings.metric.archived_questions"):int(unit["archived_questions"] or 0),
            tr("settings.table.status"):"OK" if int(unit["active_questions"] or 0)>0 else tr("settings.unit.no_active_question"),
        } for unit in active_units])
        st.dataframe(unit_df,use_container_width=True,hide_index=True)
    else:
        st.warning(tr("settings.no_active_unit"))
    b1,b2,b3=st.columns(3)
    b1.button(tr("settings.manage_units"),use_container_width=True,key="admin_units",on_click=navigate,args=(PAGE_LEARNING_UNITS,))
    b2.button(tr("settings.open_questions"),use_container_width=True,key="admin_questions",on_click=navigate,args=(PAGE_QUESTION_POOL,))
    b3.button(tr("settings.import_export"),use_container_width=True,key="admin_import_export",on_click=navigate,args=(PAGE_IMPORT_EXPORT,))

    st.divider()
    st.subheader(tr("settings.rounds.title"))
    round_rows=dashboard_round_status(conn)
    if round_rows:
        round_table=[]
        for rnd in round_rows:
            row={
                tr("settings.rounds.col.round"):rnd["name"],
                tr("settings.rounds.col.questions"):f"{rnd['n_questions']}/8",
                tr("settings.rounds.col.status"):tr("settings.rounds.playable") if rnd["playable"] else tr("settings.rounds.incomplete"),
            }
            row.update({code:coverage_state_label(state) for code,state in rnd["coverage"].items()})
            round_table.append(row)
        st.dataframe(pd.DataFrame(round_table),use_container_width=True,hide_index=True)
    else:
        st.warning(tr("settings.no_rounds"))
    st.button(tr("settings.manage_rounds"),key="admin_rounds",on_click=navigate,args=(PAGE_ROUNDS,))

    st.divider()
    st.subheader(tr("settings.game.title"))
    if selected_course_id is None:
        st.info(tr("settings.game.need_course"))
    else:
        running=course_status["running_game"] if course_status else None
        mode_key=f"next_player_mode_{selected_course_id}"
        if mode_key not in st.session_state:
            st.session_state[mode_key]="random"
        if running:
            running_game=get_game(conn,int(running["id"]))
            player=current_player(conn,running_game)
            c1,c2,c3=st.columns(3,border=True)
            c1.metric(tr("settings.game.running"),running_game["round_name"])
            c2.metric(tr("settings.game.score"),f"{running_game['team1_points']} : {running_game['team2_points']}")
            c3.metric(tr("settings.game.active_team"),team_name(running_game["current_team"]) if running_game["current_team"] else "–")
            if player:
                st.write(tr("settings.game.current_player", name=player["display_name_snapshot"], team=player["team_snapshot"]))
            running_mode="random" if running_game["player_selection_mode"]=="random" else "manual"
            st.radio(
                tr("settings.player_mode.label"), ["random","manual"], index=0 if running_mode=="random" else 1,
                format_func=player_mode_label, horizontal=True, disabled=True, key=f"running_mode_{running_game['id']}",
            )
            st.caption(tr("settings.player_mode.locked"))
            st.button(tr("settings.game.resume"),type="primary",key=f"admin_resume_{running_game['id']}",on_click=navigate,args=(PAGE_GAME,int(running_game["id"])))
        else:
            current_mode=st.session_state[mode_key]
            selected_mode=st.radio(
                tr("settings.player_mode.label"), ["random","manual"], index=0 if current_mode=="random" else 1,
                format_func=player_mode_label, horizontal=True, key=f"player_mode_control_{selected_course_id}", help=tr("settings.player_mode.help"),
            )
            st.session_state[mode_key]=selected_mode
            st.caption(tr("settings.player_mode.random_caption") if selected_mode=="random" else tr("settings.player_mode.manual_caption"))
            st.button(tr("settings.game.prepare"),key="admin_new_game",on_click=navigate,args=(PAGE_GAME,))

    st.divider()
    st.subheader(tr("settings.aborted.title"))
    aborted_games=list_games(conn,"aborted")
    if not aborted_games:
        st.info(tr("settings.aborted.none"))
    else:
        aborted_labels={
            tr(
                "settings.aborted.option",
                round_name=g["round_name"],
                course_code=g["course_code"],
                team1=g["team1_points"],
                team2=g["team2_points"],
            ):int(g["id"])
            for g in aborted_games
        }
        aborted_label=st.selectbox(
            tr("settings.aborted.select"),
            list(aborted_labels),
            key="settings_aborted_select",
        )
        aborted_id=aborted_labels[aborted_label]
        aborted_game=next(g for g in aborted_games if int(g["id"])==aborted_id)
        delete_confirm_key=f"delete_aborted_confirm_{aborted_id}"
        if st.button(tr("settings.aborted.delete"),key=f"delete_aborted_{aborted_id}",type="secondary"):
            st.session_state[delete_confirm_key]=True
            rerun()
        if st.session_state.get(delete_confirm_key):
            st.warning(tr(
                "settings.aborted.warning",
                round_name=aborted_game["round_name"],
                course_code=aborted_game["course_code"],
            ))
            delete_yes,delete_no=st.columns(2)
            if delete_yes.button(tr("settings.aborted.confirm"),key=f"delete_aborted_confirm_btn_{aborted_id}",type="primary"):
                try:
                    deleted_round=aborted_game["round_name"]
                    deleted_course=aborted_game["course_code"]
                    delete_aborted_game(conn,aborted_id)
                    st.session_state.pop(delete_confirm_key,None)
                    st.session_state["game_delete_success"]={"round_name":deleted_round,"course_code":deleted_course}
                    rerun()
                except Exception as e:
                    show_error(e)
            if delete_no.button(tr("settings.aborted.cancel"),key=f"delete_aborted_cancel_{aborted_id}"):
                st.session_state.pop(delete_confirm_key,None)
                rerun()


elif PAGE==PAGE_ACCOUNT:
    st.title(tr("account.title"))
    st.write(tr("account.signed_in", username=st.session_state.get("username")))
    with st.form("username"):
        new_user=st.text_input(tr("account.new_username"),value=st.session_state.get("username"))
        pw_for_user=st.text_input(tr("account.confirm_password"),type="password",key="pw_user")
        if st.form_submit_button(tr("account.change_username")):
            ok,msg,new_display=change_username(conn,st.session_state.get("username"),pw_for_user,new_user)
            (st.success if ok else st.error)(tr(msg))
            if ok:
                st.session_state.username=new_display
                rerun()
    st.divider()
    with st.form("pw"):
        old=st.text_input(tr("account.old_password"),type="password")
        new=st.text_input(tr("account.new_password"),type="password")
        confirm=st.text_input(tr("account.new_password_repeat"),type="password")
        if st.form_submit_button(tr("account.change_password")):
            ok,msg=change_password(conn,st.session_state.get("username"),old,new,confirm)
            (st.success if ok else st.error)(tr(msg))
