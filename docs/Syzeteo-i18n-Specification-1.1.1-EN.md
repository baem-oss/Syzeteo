# Syzeteo – Internationalization Specification 1.1.1

Date: 2026-09-10

## 1. Goal

Syzeteo 1.1.1 keeps English and German as the two official UI languages and strengthens the catalog architecture so optional local presentation profiles can be installed without changing domain logic, the data model, or game rules.

## 2. Official catalogs

```text
locales/
  en.json
  de.json
  README.md
```

- `en` is the reference and fallback language.
- `de` is the German Syzeteo UI.
- Both official catalogs contain the same keys and compatible placeholder contracts.

The public release does not ship personalized presentation profiles.

## 3. Optional local profiles

Administrators may add a complete local catalog such as `de_custom.json`. Such a profile changes presentation strings only. Internal card types, status codes, team IDs, scoring rules, database structures, and Question Pool formats remain language-neutral.

## 4. Locale resolution

Locale identifiers with an explicitly installed catalog are preserved in full. Thus an installed `de_custom` catalog resolves as `de_custom` rather than collapsing to `de`. Ordinary regional tags such as `de-DE` continue to fall back to `de` when no exact catalog exists.

## 5. Persistence

Any installed locale can be selected on the login page and stored as `ui_locale` in Instructor Settings. The selected locale survives restarts as long as the corresponding catalog remains installed.

## 6. Language-neutral boundaries

A locale selection does not change:

- SQLite schema or schema version;
- database file or data path;
- internal team identifiers;
- card or status codes;
- game/scoring rules;
- course, team, student, round, question, or answer content;
- the technical Question Pool JSON format `Syzeteo question pool`.

## 7. Challenge Card rendering

The revealed Challenge Card obtains both its title and subtitle from the active catalog. Hard-coded UI literals are not permitted on that rendering path.

## 8. Acceptance tests

The automated suite verifies that:

- `en` and `de` have exactly the same key set;
- placeholders are compatible;
- explicitly installed compound locales are preserved;
- regional tags still fall back to their base language when appropriate;
- optional profiles can override presentation values and persist as `ui_locale`;
- the revealed Challenge Card uses translation keys instead of hard-coded English literals.
