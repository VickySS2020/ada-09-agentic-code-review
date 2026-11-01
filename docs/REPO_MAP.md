# Repository Map

## Entry Points
- `src/cli.py` - CLI entry point; parses arguments such as `--name`, `--email`, `--query`, and `--file`, and renders results.
- `src/service.py` - Customer search and business logic (query validation, filtering, and matching).
- `src/models.py` - Customer domain model and customer data representation.
- `src/storage.py` - Loads customer records from local JSON and handles data-loading errors.
- `customers.json` - Local customer dataset.
- `README.md` - Setup instructions, CLI usage examples, and test commands.

## Tests
- `tests/` - Automated tests for the application.

## Change Guide
If changing customer search behavior:
1. Check `REQUIREMENTS.md` and `SPEC.md` for the intended behavior and acceptance criteria.
2. Update `src/service.py` when search or validation logic changes.
3. Update `src/storage.py` only when data loading or storage behavior changes.
4. Update `src/cli.py` when CLI arguments, command handling, or displayed output changes.
5. Update or add relevant tests under `tests/`.
6. Update `README.md` if CLI arguments or usage instructions change.
7. Run `python -m pytest -v`.
8. Run `./scripts/verify_repo.sh` if the script exists in the current checkout. If it is missing, report that the verification script could not be run.

## Do Not Edit Directly
- `.env` or files containing secrets or credentials.
- Generated files or test evidence under `results/`, unless the task specifically requires regenerating them.
- Unrelated files outside the requested scope.