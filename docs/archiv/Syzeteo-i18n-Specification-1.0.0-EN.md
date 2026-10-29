# Syzeteo – Internationalization Specification 1.0.0

Date: 2026-08-27

## 1. Goal

Syzeteo 1.0.0 ships with a clean and extensible internationalization layer for the complete application UI. English and German are included initially. Additional languages must be addable through locale catalogs without changing domain logic.

## 2. Architecture

### 2.1 Files

```text
locales/
  en.json
  de.json
  README.md
i18n.py
```

English (`en`) is the reference and fallback catalog.

### 2.2 Translation function

Application code references stable translation keys through the central translation layer. UI control flow must never depend on translated labels.

### 2.3 Placeholders

Placeholders are named and must remain compatible across catalogs, for example:

```json
"course.label": "Course {code}"
```

A translated value for the same key must expose the same placeholder names.

## 3. Mandatory requirements

### I18N #01 – English reference locale

English (`en`) is the reference and fallback language.

### I18N #02 – Complete German locale

The German catalog (`de`) contains the same key set as the English catalog.

### I18N #03 – External catalogs

UI texts are stored in UTF-8 JSON catalogs outside the application logic.

### I18N #04 – Fallback

If a key is missing from a non-reference catalog, the English value is used. Unknown locales fall back to English.

### I18N #05 – Persistent locale selection

The chosen default UI locale can be persisted as the language-neutral application setting `ui_locale`.

### I18N #06 – Locale selection before login

A locale can be selected on login/first-run before authentication. This choice applies to the current session.

### I18N #07 – Restricted selector locations

The language selector is available only on login/first-run and in Instructor Settings. It is not shown in the sidebar or on the Account page.

### I18N #08 – Stable navigation IDs

Navigation logic uses language-neutral page IDs such as `dashboard`, `courses`, `students`, `game`, and `instructor_settings`.

### I18N #09 – Language-neutral domain/status codes

Persisted values, status codes, configuration issue identifiers and domain error codes are language-neutral.

### I18N #10 – No localized storage messages

`storage.py` emits language-neutral `StorageError` codes rather than user-facing translated messages.

### I18N #11 – No localized authentication logic

Authentication logic remains independent of locale-specific UI strings.

### I18N #12 – Structured configuration issues

Configuration warnings use stable codes and parameters; presentation text is produced by the UI translation layer.

### I18N #13 – User content is not translated

Question Pool content, course names, student names, round names and other user-provided content are never automatically translated.

### I18N #14 – Technical interfaces remain language-neutral

Database schema identifiers, page IDs, setting keys and internal domain values do not change with UI locale.

### I18N #15 – Stable exchange formats

The Syzeteo Question Pool JSON format is language-neutral. Student CSV import supports English headers `first_name` / `last_name` and German headers `vorname` / `nachname`.

### I18N #16 – Community translations

Additional locale catalogs may be added if they preserve the reference key set and placeholder contracts.

## 4. Locale selection and persistence

- new installations default to English;
- login/first-run selection affects the current session;
- Instructor Settings can persist the default locale;
- a valid persisted locale is reused on later logins;
- an unavailable or invalid locale falls back to English.

## 5. Acceptance tests

The automated suite must verify at least:

- official catalogs are valid UTF-8 JSON;
- English and German have identical key sets;
- placeholder sets match;
- missing translations fall back to English;
- unknown locales fall back to English;
- navigation uses stable page IDs;
- configuration actions use language-neutral IDs;
- selector locations are restricted to login/first-run and Instructor Settings;
- `ui_locale` persists correctly;
- known German UI literals are absent from application control flow;
- storage error keys and configuration issue keys exist in both official catalogs;
- every literal translation key referenced by `app.py` exists in the English catalog;
- every literal `StorageError` key referenced by `storage.py` exists in the English catalog.

## 6. Current catalog baseline

Syzeteo 1.0.0 ships with **473 translation keys** in each official catalog. The key sets are identical.

## 7. Definition of Done

Internationalization is complete for Syzeteo 1.0.0 when:

1. every application page is usable in English and German;
2. English is the reference/fallback language;
3. the two official catalogs have identical keys and compatible placeholders;
4. locale selection is available only at the defined locations;
5. the saved default locale persists correctly;
6. user-provided Question Pool content is never translated automatically;
7. domain and persistence logic remain language-neutral; and
8. the complete automated test suite passes.
