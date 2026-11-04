# Human Review Decisions
## Change
CR-01

### RF-01
Reviewer severity: MUST FIX

Human decision: ACCEPTED

Reason: The finding well justifies a missing gap in test coverage at the CLI presentation layer that ensures invalid customer record data yields a readable error and exits cleanly without an unhandled traceback.

The coder report masked this gap by pointing to a preexisting-file test.

Required action: Add a test in `tests/test_cli.py` (e.g., `test_cli_invalid_customer_record_handled_gracefully(tmp_path, capsys)`) that writes a temporary JSON file with an invalid record (e.g. `{"id": 1, "name": "   ", "email": "a@b.com"}`), invokes `main(["--file", str(bad_file), "--name", "Alice"])`, asserts exit code 1, and verifies that `captured.out` contains `ERROR: Failed to load customer records: invalid record at index 0` without an unhandled traceback.

### RF-02
Reviewer severity: SHOULD FIX

Human decision: ACCEPTED

Reason: This was an issue found in the previous activity, but it was not treated due to being out of the scope for said activity.

Required action: Untrack all `__pycache__` directories using `git rm -r --cached src/__pycache__ tests/__pycache__`, and commit a root `.gitignore` file ignoring `__pycache__/`, `*.pyc`, and `.pytest_cache/`.

### RF-03
Reviewer severity: SHOULD FIX

Human decision: REJECTED

Reason: The `verification-report.md` was written by the student, not the coder agent who wrote `coder-report.md`. The command ./scripts/verify_repo.sh was executed succesfully by the student, and manually by the coder, so the documentation is still consistent.

### RF-04
Reviewer severity: SHOULD FIX

Human decision: MODIFIED

Reason: None of the 9 new CR-01 test cases in `tests/test_storage.py` are listed in `docs/traceability.md`.

Required action: Update row FR-07 in `docs/traceability.md` to include the new unit/storage validation test cases inside `tests/test_storage.py` under "Test" column.

### RF-05
Reviewer severity: OPTIONAL

Human decision: REJECTED

Reason: The current implementation is sufficient for this project's scope.

## Human Gate
[X] Return to coder-agent

[ ] Ready for final re-review

[ ] Stop / escalate
