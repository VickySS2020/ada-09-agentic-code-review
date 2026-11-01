# Tasks

## T-01 Project setup
- Goal: Create project structure and configure environment.
- Files: src/, tests/, customers.json
- Acceptance: pytest can execute and environment satisfies NFR-01, NFR-05, C-01, C-02, and C-03.
- Verification: pytest -v

## T-02 Domain model
- Goal: Implement Customer model and JSON storage loader.
- Files: src/models.py, src/storage.py, customers.json, tests/test_storage.py
- Acceptance: AC-07, VR-03, EH-04, and C-04 are satisfied.
- Verification: persistence tests pass.

## T-03 Search logic
- Goal: Implement search by name, email, and unified query, and display results in CLI.
- Files: src/service.py, src/cli.py, tests/test_service.py
- Acceptance: AC-01, AC-02, AC-04, AC-06, AC-08, SR-01, SR-02, SR-03, and NFR-02 pass.
- Verification: tests + manual CLI run.

## T-04 Validation and errors
- Goal: Implement search query validation, command-line argument validation, and error messaging.
- Files: src/service.py, src/cli.py, tests/test_validation.py
- Acceptance: VR-01, VR-02, EH-01, EH-02, EH-03, AC-03, and AC-05 pass.
- Verification: validation tests pass.

## T-05 Tests
- Goal: Implement automated test suite covering service, storage, and CLI.
- Files: tests/test_service.py, tests/test_storage.py, tests/test_cli.py
- Acceptance: TS-01 through TS-11 pass and NFR-03 is satisfied.
- Verification: pytest -v

## T-06 Documentation
- Goal: Update requirements traceability, AI Usage log and other project documents.
- Files: README.md, docs/traceability.md, AI_USAGE_LOG.md
- Acceptance: Requirements coverage (FR-01 through FR-07, NFR-01 through NFR-05) and test traceability are complete.
- Verification: review documentation against specification.
