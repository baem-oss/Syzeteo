"""Rendering helpers for literal question and answer content.

Question and answer texts are user-managed content. They must be displayed
verbatim and must not acquire Markdown semantics merely because Streamlit
renders labels or text through Markdown-capable widgets.
"""

import html
import re


_MARKDOWN_SPECIAL = re.compile(r"([\\`*_{}\[\]<>\(\)#+\-.!|>$~])")


def escape_markdown_literal(text: str) -> str:
    """Escape Markdown control characters while preserving visible text.

    This is intended for Markdown-capable widget labels (notably st.button),
    where raw question text such as ``7. Example`` could otherwise become a
    list item and lose or change its visible numbering.
    """
    return _MARKDOWN_SPECIAL.sub(r"\\\1", str(text or ""))


def round_question_html(position, unit_code: str, question_text: str) -> str:
    """Return safe HTML for a question in the round overview.

    The round position is intentionally rendered as the outer numbering, while
    the complete stored question text is escaped and preserved literally. This
    prevents numbered lines inside a question from being reinterpreted or
    renumbered by Markdown.
    """
    safe_position = html.escape(str(position))
    safe_unit = html.escape(str(unit_code or ""))
    safe_question = html.escape(str(question_text or ""))
    return (
        "<div class='syzeteo-round-question' "
        "style='white-space: pre-wrap; overflow-wrap: anywhere;'>"
        f"{safe_position}. <strong>{safe_unit}</strong> – {safe_question}</div>"
    )


def plain_text_html(text: str) -> str:
    """Return safe HTML that displays multiline text literally.

    HTML special characters are escaped and line breaks/spacing are preserved.
    The caller may pass the result to ``st.markdown(..., unsafe_allow_html=True)``.
    """
    safe = html.escape(str(text or ""))
    return (
        "<div class='syzeteo-literal-text' "
        "style='white-space: pre-wrap; overflow-wrap: anywhere;'>"
        f"{safe}</div>"
    )
