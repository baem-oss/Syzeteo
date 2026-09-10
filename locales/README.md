# Syzeteo translation catalogs

Syzeteo uses UTF-8 JSON catalogs in this directory. English (`en.json`) is the reference and fallback catalog.

Official catalogs shipped with Syzeteo 1.1.1:

- `en.json` – English reference/fallback;
- `de.json` – German Syzeteo UI.

Optional local presentation profiles or additional languages can be added without changing domain logic:

1. Copy `en.json` to `<locale>.json`, for example `fr.json` or `de_custom.json`.
2. Translate or personalize values only. Keep every key unchanged.
3. Preserve all named placeholders exactly (for example `{code}`).
4. Keep the file valid UTF-8 JSON.
5. Run `python -m unittest discover -v` before deployment.

An explicitly installed compound locale such as `de_custom` is preserved as its own locale. Ordinary regional tags such as `de-DE` fall back to the base language if no exact catalog exists.

Translation keys, stable page IDs, database values, card types, scoring rules, the SQLite schema, and the Question Pool interchange format are language-neutral. Application/domain data such as course names, team names, learning units, questions and model answers are user content and are not translated by these catalogs.
