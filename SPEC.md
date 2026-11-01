# Customer Search Feature

## Goal
Provide a simple CLI tool to search customer records by name or email with case-insensitive partial matching, input validation, and local JSON file persistence.

## Requirements Covered
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- FR-07
- NFR-01
- NFR-02
- NFR-03
- NFR-04
- NFR-05

## Scope
- Search customer records by name (`--name`), email (`--email`), or unified query (`--query`).
- Case-insensitive partial matching on search terms.
- Input validation to reject empty or whitespace-only search queries.
- Display all matching customer records to the user.

## Out of Scope
- Graphical user interface (GUI) or web interface.
- Modifying customer records (creation, update, deletion).
- External database engines (e.g., PostgreSQL, SQLite) or cloud storage.
- External API calls or network communication.
- Multi-user authentication, roles, or authorization.

## Domain Model
Customer:
- id: int
- name: str (full customer name)
- email: str (customer email address)
Storage:
- JSON file: `customers.json`

## Search Rules
- SR-01 [FR-01]: Name search matches if the query is a case-insensitive substring of the customer's name (e.g., "ali" matches "Alice Smith").
- SR-02 [FR-02]: Email search matches if the query is a case-insensitive substring of the customer's email (e.g., "alice@" or "example.com" matches "alice@example.com").
- SR-03 [FR-06]: Supports field-specific searches (`--name <term>`, `--email <term>`) or a general search (`--query <term>` matching against either name or email).

## Validation Rules
- VR-01 [FR-03]: Search query is required and cannot be empty or whitespace-only after stripping leading and trailing whitespace.
- VR-02 [FR-03, FR-06]: At least one search argument must be supplied when executing a search with a command-line argument (`--name`, `--email`, or `--query`).
- VR-03 [FR-07]: Customer data source file must be valid JSON formatted as a list of objects containing required customer attributes (`id`, `name`, `email`).

## Error Handling
- EH-01 [FR-03]: If a search query is empty or contains only whitespace, output `ERROR: Invalid Input` and terminate without crashing.
- EH-02 [FR-06]: If invalid flags are passed or required search options are omitted, display CLI instructions/options and exit.
- EH-03 [FR-05]: If no customer records match the search query, output `MESSAGE: No customers found that matched <query>` and exit.
- EH-04 [FR-07]: If the JSON file is missing, inaccessible, or contains malformed JSON, display a descriptive error message (e.g., `ERROR: Failed to load customer records: <details>`) and exit without an unhandled stack trace.

## Acceptance Criteria
- AC-01 [FR-01, FR-06]: Users can search customers by name using partial, case-insensitive matching and receive all matching records.
- AC-02 [FR-02, FR-06]: Users can search customers by email using partial, case-insensitive matching and receive all matching records.
- AC-03 [FR-03]: Empty or whitespace-only search terms are rejected with the error message `ERROR: Invalid Input`.
- AC-04 [FR-04]: Matching records are displayed in a structured table displaying ID, Name, and Email columns.
- AC-05 [FR-05]: When a query yields no matching customers, the CLI outputs `MESSAGE: No customers found that matched <query>`.
- AC-06 [FR-06]: The CLI provides a `--query` flag that searches for customers with an email and/or name that partially match the query.
- AC-07 [FR-07]: Customer records are successfully read and parsed from a local JSON file (`customers.json`).
- AC-08 [NFR-04]: Search operations executed against the local customer dataset complete with a response time of under 100 milliseconds.

## Test Scenarios
TS-01 -> AC-01 | TS-02 -> AC-02 | TS-03 -> AC-03 | TS-04 -> AC-04
TS-05 -> AC-05 | TS-06 -> AC-06 | TS-07 -> AC-07 | TS-08 -> AC-08
TS-09 -> VR-01 | TS-10 -> VR-02 | TS-11 -> VR-03

## Constraints
- C-01 [NFR-05]: Implementation must be compatible with Python 3.11+.
- C-02 [NFR-01]: Zero external production dependencies; standard library modules only.
- C-03 [NFR-03]: Automated tests must be implemented and executable using `pytest`.
- C-04 [FR-07]: Customer records must be stored and loaded from a local JSON file.

## Open Questions
- Q-01: JSON File Location & Configuration — What should be the default path for the customer JSON file (e.g., `customers.json` in the project root), and should users be able to pass a custom file path via a CLI option (e.g., `--file <path>`)?
- Q-02: Combined vs. Specific Search — Should the CLI support a unified search flag (e.g., `--query <term>` that searches across both name and email simultaneously), or should it enforce searching by one attribute at a time?
- Q-03: Customer Record Schema — What are the required and optional fields for a customer record (e.g., `id`, `name`, `email`, `phone`, `status`)?
- Q-04: CLI Interaction Mode — Is the CLI intended solely as a one-shot command (e.g., `python -m ... --name Bob`), or should it also support an interactive prompt loop?
