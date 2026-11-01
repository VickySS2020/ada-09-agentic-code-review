# Architecture

## Overview
The Customer Search application follows a modular, three-tier architecture built with Python 3.11+ standard libraries. The architecture decouples presentation, business logic, and storage to ensure high testability.

## Components
The system consists of three distinct layers:
1. **CLI Layer**: Interprets command-line arguments and flags, invokes the service layer, and presents formatted results and error messages to the user.
2. **Customer Service Layer**: Applies domain business logic, search query validation, case-insensitive partial matching, and search coordination.
3. **Storage Layer (`customers.json`)**: Reads, parses, and returns customer records from the local `customers.json` file.

## Responsibilities
- **CLI**:
  - Parse command-line flags (`--name`, `--email`, `--query`).
  - Delegate search requests to `CustomerService`.
  - Format and render matching customer records in a readable table (`ID`, `Name`, `Email`).
  - Render user-friendly messages for no matches and error notifications.
- **Customer Service**:
  - Validate search query inputs (ensure non-empty, non-whitespace after trimming).
  - Execute partial substring searches across customer names and emails.
  - Filter customer records based on query parameters.
- **Storage (`customers.json`)**:
  - Read and parse `customers.json` into memory using Python's built-in `json` module.
  - Validate file existence and JSON structure/schema integrity.
  - Handle missing or malformed file exceptions gracefully and raise domain-appropriate errors.

## Data Flow
1. User runs a CLI command (e.g., `python -m customer_search --name Alice`).
2. CLI parses arguments and calls `CustomerService`.
3. `CustomerService` validates search query and business rules.
4. Storage reads and returns data from `customers.json`.
5. `CustomerService` performs case-insensitive partial matching on customer records.
6. Matching records or empty result indicators return to the CLI.
7. CLI formats and displays the results table or message to the user.

## Interfaces
- **Customer Entity**:
  - `id`: `int`
  - `name`: `str` (full customer name)
  - `email`: `str` (customer email address)
- **Storage Interface**:
  - `load_customers(file_path: str = "customers.json") -> list[dict]`
- **CustomerService Interface**:
  - `search_by_name(query: str) -> list[dict]`
  - `search_by_email(query: str) -> list[dict]`
  - `search(query: str) -> list[dict]` (searches both name and email)
  - `validate_query(query: str) -> str`

## Error Handling
- Validation belongs to the service layer; CLI renders clear messages.
- Empty or whitespace-only inputs trigger validation errors in the service, which the CLI presents as `ERROR: Invalid Input`.
- Storage issues (missing file, invalid JSON syntax, corrupt schema) raise domain-specific storage exceptions caught by the CLI to display clean error messages without raw stack traces.
- When no records match, the service returns an empty list, and the CLI renders `MESSAGE: No customers found that matched <query>`.

## Testing Strategy
- **Unit tests for service**: Test `CustomerService` in isolation using mock customer data to verify query validation, case-insensitive partial substring matching, and edge cases.
- **Persistence tests for storage**: Test `Storage` with valid, empty, missing, and malformed JSON files to verify parsing and error handling.
- **Minimal CLI verification**: Test CLI argument parsing (`--name`, `--email`, `--query`) and output rendering using `pytest` with capsys/monkeypatch.

## Dependencies
- **Runtime**: Python standard library only (`argparse`, `json`, `sys`, `pathlib`, `typing`). No external production packages or APIs.
- **Development/Testing**: `pytest` for automated test execution.
- **Target Environment**: Python 3.11+.

## Design Decisions
- **Decouple business logic from CLI**: Keep business logic independent from CLI for testability and maintainability.
- **Pure Standard Library**: Use built-in `argparse` and `json` to fulfill zero-external-dependencies requirement (NFR-01).
- **In-Memory Search**: Read records into memory for fast linear scanning to meet the sub-100ms response time requirement (NFR-04, AC-08).

## Trade-offs
- **In-Memory Scanning vs. Indexed Search**: Loading all records from `customers.json` into memory is simple, dependency-free, and fast for small-to-medium datasets, but not optimized for millions of records.
- **JSON Flat File vs. SQLite**: Flat JSON file satisfies simplicity and human-readability without external drivers, but lacks concurrent write handling (acceptable since record modification is out of scope).
- **Standard `argparse` vs. Third-Party Frameworks (`click`/`typer`)**: Requires manual formatting for tables and errors, but eliminates external dependencies.
