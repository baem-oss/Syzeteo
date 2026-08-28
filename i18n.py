import json
import os
import string
from functools import lru_cache
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent / "locales"
DEFAULT_LOCALE = "en"
ENV_LOCALE = "SYZETEO_LOCALE"


class I18nError(RuntimeError):
    """Raised when a translation catalog is invalid or cannot satisfy a strict lookup."""


def _catalog_path(locale: str) -> Path:
    return LOCALES_DIR / f"{locale}.json"


def normalize_locale(locale: str | None) -> str:
    value = (locale or "").strip().lower().replace("-", "_")
    if not value:
        return DEFAULT_LOCALE
    return value.split("_", 1)[0]


@lru_cache(maxsize=None)
def load_catalog(locale: str) -> dict[str, str]:
    locale = normalize_locale(locale)
    path = _catalog_path(locale)
    if not path.exists():
        raise I18nError(f"Translation catalog not found: {locale}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise I18nError(f"Invalid translation catalog: {locale}") from exc
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise I18nError(f"Translation catalog must contain string keys and values: {locale}")
    return data


def available_locales() -> list[str]:
    if not LOCALES_DIR.exists():
        return [DEFAULT_LOCALE]
    locales = sorted(p.stem for p in LOCALES_DIR.glob("*.json") if p.is_file())
    if DEFAULT_LOCALE in locales:
        locales.remove(DEFAULT_LOCALE)
        locales.insert(0, DEFAULT_LOCALE)
    return locales or [DEFAULT_LOCALE]


def locale_display_name(locale: str) -> str:
    locale = normalize_locale(locale)
    catalog = load_catalog(locale)
    return catalog.get("language.name", locale)


def initial_locale() -> str:
    requested = normalize_locale(os.environ.get(ENV_LOCALE))
    return requested if requested in available_locales() else DEFAULT_LOCALE


def _fields(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


def t(key: str, *, locale: str | None = None, strict: bool = False, **params) -> str:
    active = normalize_locale(locale)
    try:
        catalog = load_catalog(active)
    except I18nError:
        catalog = load_catalog(DEFAULT_LOCALE)
        active = DEFAULT_LOCALE

    template = catalog.get(key)
    if template is None and active != DEFAULT_LOCALE:
        template = load_catalog(DEFAULT_LOCALE).get(key)
    if template is None:
        if strict:
            raise I18nError(f"Missing translation key: {key}")
        return key

    try:
        return template.format(**params)
    except (KeyError, IndexError, ValueError) as exc:
        if strict:
            raise I18nError(f"Invalid translation parameters for key: {key}") from exc
        return template


def validate_catalogs(required_locales: tuple[str, ...] = ("en", "de")) -> list[str]:
    errors: list[str] = []
    reference = load_catalog(DEFAULT_LOCALE)
    reference_keys = set(reference)

    for locale in required_locales:
        catalog = load_catalog(locale)
        keys = set(catalog)
        missing = sorted(reference_keys - keys)
        extra = sorted(keys - reference_keys)
        if missing:
            errors.append(f"{locale}: missing keys: {', '.join(missing)}")
        if extra:
            errors.append(f"{locale}: extra keys: {', '.join(extra)}")
        for key in sorted(reference_keys & keys):
            if _fields(reference[key]) != _fields(catalog[key]):
                errors.append(f"{locale}: placeholder mismatch for {key}")
    return errors
