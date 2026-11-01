# Requirements — Customer Search

## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements
FR-01: Search by Name — The CLI must allow users to search customer records by name. The search must support case-insensitive partial substring matching (e.g., searching "ali" matches "Alice Smith").
FR-02: Search by Email — The CLI must allow users to search customer records by email address. The search must support case-insensitive partial substring matching (e.g., searching "example" or "alice@" matches "alice@example.com").
FR-03: Search Query Validation — The CLI must validate user search queries prior to execution. Empty strings and whitespace-only inputs must be rejected with a user-friendly error message ("ERROR: Invalid Input") without crashing.
FR-04: Display Results — The CLI must display all matching customer records in a clear, readable table showing relevant fields (e.g., ID, Name, Email).
FR-05: No Matches Handling — When no customer records match the given query, the CLI must output an informative message ("MESSAGE: No customers found that matched <query>").
FR-06: CLI Options — The CLI must support standard command-line flags/arguments (e.g., `--name`, `--email`, `--query`).
FR-07: Customer Data Loading — Customer records must be stored in and loaded from a local JSON file.

## Non-Functional Requirements
NFR-01: Zero External Runtime Dependencies — The application must run using only Python standard libraries (e.g., `argparse`, `json`, `csv`, `re`), with no external third-party production packages or external APIs.
NFR-02: Separation of Business Logic — Core business logic (query validation, search, filtering) must be separate from CLI presentation.
NFR-03: Automated Testability — Core business logic (query validation, search, filtering) must be fully testable using `pytest`.
NFR-04: Performance — Search operations over local customer datasets must execute with near-instantaneous response times (< 100 ms).
NFR-05: Python Compatibility — The codebase must be compatible with Python 3.11+.

## Open Questions
Q-01: JSON File Location & Configuration — What should be the default path for the customer JSON file (e.g., `customers.json` in the project root), and should users be able to pass a custom file path via a CLI option (e.g., `--file <path>`)?
Q-02: Combined vs. Specific Search — Should the CLI support a unified search flag (e.g., `--query <term>` that searches across both name and email simultaneously), or should it enforce searching by one attribute at a time?
Q-03: Customer Record Schema — What are the required and optional fields for a customer record (e.g., `id`, `name`, `email`, `phone`, `status`)?
Q-04: CLI Interaction Mode — Is the CLI intended solely as a one-shot command (e.g., `python -m ... --name Bob`), or should it also support an interactive prompt loop?

## Constraints / Assumptions
C-01: Language & Environment — Implemented in Python targeting version 3.11 or higher.
C-02: No External Dependencies/APIs — No third-party production packages or network calls; standard library only. `pytest` is permitted exclusively as a development/testing dependency.
C-03: Test Framework — Automated tests must execute cleanly using the command `pytest`.
C-04: Local Storage Format — Customer records must be stored in and retrieved from a local JSON file.
A-01: Case-Insensitive Matching — All partial name and email searches are assumed to be case-insensitive by default.
A-02: Data Size — The customer dataset is assumed to fit entirely in memory for fast retrieval.
A-03: Input Sanitization — Leading and trailing whitespace in search inputs is assumed to be trimmed automatically.
