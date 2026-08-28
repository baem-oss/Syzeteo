# Contributing to Syzeteo

Thank you for considering a contribution to Syzeteo.

## Development setup

1. Create a Python virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Run the test suite with `python -m unittest discover -v`.
4. Run the application with `streamlit run app.py`.

## Requirements and schema discipline

Syzeteo is requirements-driven. Changes to game behavior should preserve the IDs and traceability relationships documented in `docs/` or update the specification and tests together with the implementation.

Syzeteo 1.0.0 defines database schema version 2. Persisted domain identifiers are part of the technical contract. Schema changes must increment the schema version and provide an explicit, tested migration path for released Syzeteo databases.

## Pull requests

A pull request should:

- describe the behavioral change;
- add or update tests for changed behavior;
- keep all existing tests passing;
- avoid committing databases, WAL/SHM files, backups, real student data, credentials or non-redistributable teaching content;
- update the German and English specification when a normative rule changes.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0 used by this project.
