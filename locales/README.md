# Syzeteo translation catalogs

Syzeteo uses UTF-8 JSON catalogs in this directory. English (`en.json`) is the reference and fallback catalog.

To add a language:

1. Copy `en.json` to `<locale>.json`, for example `fr.json`.
2. Translate values only. Keep every key unchanged.
3. Preserve all named placeholders exactly (for example `{code}`).
4. Keep the file valid UTF-8 JSON.
5. Run `python -m unittest discover -v` before opening a pull request.

Application/domain data such as course names, learning units, questions and model answers are user content and must not be translated in these catalogs.
