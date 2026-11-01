"""Automated CLI test suite (T-05, TS-01 through TS-11)."""
import json
import pytest
from pathlib import Path

from src.cli import format_table, main


def test_cli_search_by_name_renders_table(capsys):
    """Verify searching by name displays a structured table (TS-01, TS-04, AC-01, AC-04)."""
    exit_code = main(["--name", "Alice"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "| ID | Name" in captured.out
    assert "| Email" in captured.out
    assert "Alice Smith" in captured.out
    assert "alice@example.com" in captured.out


def test_cli_search_by_email_renders_table(capsys):
    """Verify searching by email displays matching customer table (TS-02, TS-04, AC-02, AC-04)."""
    exit_code = main(["--email", "bob@example.com"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "| ID | Name" in captured.out
    assert "Bob Jones" in captured.out
    assert "bob@example.com" in captured.out


def test_cli_search_by_email_partial(capsys):
    """Verify searching by partial email matches multiple records (TS-02, AC-02)."""
    exit_code = main(["--email", "example"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Alice Smith" in captured.out
    assert "Bob Jones" in captured.out


def test_cli_unified_query_renders_table(capsys):
    """Verify unified --query searches name and email (TS-06, TS-04, AC-06, AC-04)."""
    exit_code = main(["--query", "charlie"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Charlie Brown" in captured.out
    assert "charlie@domain.com" in captured.out


def test_cli_custom_file_argument(tmp_path: Path, capsys):
    """Verify CLI loads from custom file passed via --file flag (TS-07, AC-07)."""
    custom_file = tmp_path / "custom_data.json"
    custom_records = [{"id": 99, "name": "Custom Person", "email": "custom@test.com"}]
    custom_file.write_text(json.dumps(custom_records), encoding="utf-8")

    exit_code = main(["--file", str(custom_file), "--name", "Custom"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Custom Person" in captured.out
    assert "custom@test.com" in captured.out


def test_cli_no_matches_message(capsys):
    """Verify informative message when no customers match (TS-05, AC-05, EH-03)."""
    exit_code = main(["--name", "NobodyHere"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "MESSAGE: No customers found that matched NobodyHere"


def test_cli_empty_query_rejected(capsys):
    """Verify empty query string outputs error without crashing (TS-03, TS-09, VR-01, EH-01, AC-03)."""
    exit_code = main(["--name", ""])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out.strip() == "ERROR: Invalid Input"


def test_cli_whitespace_query_rejected(capsys):
    """Verify whitespace-only query outputs error without crashing (TS-03, TS-09, VR-01, EH-01, AC-03)."""
    exit_code = main(["--query", "   "])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out.strip() == "ERROR: Invalid Input"


def test_cli_omitted_search_arguments_displays_help(capsys):
    """Verify help/instructions displayed when search argument is omitted (TS-10, VR-02, EH-02)."""
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "usage:" in captured.out or "Search customer records" in captured.out


def test_cli_storage_error_handled_gracefully(capsys):
    """Verify storage failure outputs clear error message without traceback (TS-11, VR-03, EH-04)."""
    exit_code = main(["--file", "nonexistent.json", "--name", "Alice"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ERROR: Failed to load customer records" in captured.out


def test_format_table_empty_list():
    """Verify format_table returns empty string for empty input."""
    assert format_table([]) == ""


def test_format_table_output_structure():
    """Verify table format creates aligned rows and header separator (TS-04, AC-04)."""
    sample = [
        {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
        {"id": 200, "name": "Bob", "email": "bob@example.com"},
    ]
    table = format_table(sample)
    lines = table.splitlines()
    assert len(lines) >= 5
    assert "+-" in lines[0]
    assert "| ID " in lines[1]
    assert "| Name " in lines[1]
    assert "| Email " in lines[1]
    assert "Alice Smith" in table
    assert "200" in table
