# Spec-Driven Customer Search CLI

## Project Description
The Customer Search application is a command-line tool designed to search customer records by name or email address using case-insensitive partial substring matching. It persists customer data in a local JSON file (`customers.json`) and formats matching records in a structured ASCII table.

The application adheres to a modular three-tier architecture:
1. **CLI Layer (`src/cli.py`)**: Command-line interface and presentation logic using Python standard library `argparse`.
2. **Service Layer (`src/service.py`)**: Core business domain logic, query validation, and search algorithms (`CustomerService`), completely decoupled from presentation.
3. **Storage Layer (`src/storage.py`)**: Reads, parses, and validates the JSON customer records (`Customer` entity in `src/models.py`), handling malformed or missing data gracefully.

The runtime application has zero external third-party production dependencies and targets Python 3.11+.

## Installation

### Prerequisites
- Python 3.11 or higher installed on your system.

### Setup
1. Clone or open the repository.
2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install development/testing dependencies:
   ```bash
   pip install pytest
   ```

## How to execute

Run the CLI using Python's module execution syntax:

### 1. Search by Name
Searches customer records whose name contains the search term (case-insensitive):
```bash
python -m src.cli --name Alice
```
Output:
```text
+----+-------------+-------------------+
| ID | Name        | Email             |
+----+-------------+-------------------+
| 1  | Alice Smith | alice@example.com |
+----+-------------+-------------------+
```

### 2. Search by Email
Searches customer records whose email address contains the search term (case-insensitive):
```bash
python -m src.cli --email example
```
Output:
```text
+----+-------------+-------------------+
| ID | Name        | Email             |
+----+-------------+-------------------+
| 1  | Alice Smith | alice@example.com |
| 2  | Bob Jones   | bob@example.com   |
+----+-------------+-------------------+
```

### 3. Unified Search (`--query`)
Searches customer records matching against either name or email address:
```bash
python -m src.cli --query Charlie
```
Output:
```text
+----+---------------+--------------------+
| ID | Name          | Email              |
+----+---------------+--------------------+
| 3  | Charlie Brown | charlie@domain.com |
+----+---------------+--------------------+
```

### 4. Sort Results (`--sort`)
Sort matching records alphabetically by `name` or `email` (case-insensitive). `--sort` is optional and may be combined with any search flag:
```bash
python -m src.cli --email example --sort name
```
Output:
```text
+----+-------------+-------------------+
| ID | Name        | Email             |
+----+-------------+-------------------+
| 1  | Alice Smith | alice@example.com |
| 2  | Bob Jones   | bob@example.com   |
+----+-------------+-------------------+
```

Sort by email address:
```bash
python -m src.cli --query example --sort email
```

**Accepted values:** `name`, `email`. Any other value is rejected with a usage error.

### 5. Custom Data File (`--file`)
Specify a custom customer JSON file path:
```bash
python -m src.cli --file path/to/customers.json --name Alice
```

### 5. Error & Notice Handling
- **No matches found**:
  ```text
  MESSAGE: No customers found that matched Unknown
  ```
- **Empty or whitespace search term**:
  ```text
  ERROR: Invalid Input
  ```
- **Missing or malformed data file**:
  ```text
  ERROR: Failed to load customer records: file 'missing.json' not found
  ```

## Tests

Execute the automated test suite using `pytest`:
```bash
pytest -v
```
All 62 unit, integration, persistence, validation, sorting, and CLI test scenarios will run and verify requirements compliance in under 1 second.