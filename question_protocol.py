"""Pure formatting, filtering and export helpers for US #24 question log."""
import pandas as pd


def filter_protocol_table(table: pd.DataFrame, course_column: str, round_column: str,
                          selected_courses=(), selected_rounds=()) -> pd.DataFrame:
    """Apply the same course/round selection to the displayed and exported rows."""
    result = table.copy()
    if selected_courses:
        result = result[result[course_column].isin(selected_courses)]
    if selected_rounds:
        result = result[result[round_column].isin(selected_rounds)]
    return result


def export_protocol_csv(table: pd.DataFrame) -> bytes:
    """Export exactly the displayed table, including its translated headers."""
    return table.to_csv(index=False).encode("utf-8-sig")
