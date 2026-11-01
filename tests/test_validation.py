"""Tests for search query validation, argument validation, and error messaging (T-04)."""
import pytest
from src.cli import main
from src.service import CustomerService, ValidationError


@pytest.fixture
def service():
    sample = [
        {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Jones", "email": "bob@example.com"},
    ]
    return CustomerService(customers=sample)


# ============================================================================
# VR-01, EH-01, AC-03: Query validation (empty & whitespace-only rejection)
# ============================================================================

def test_validate_query_empty_string(service):
    """Verify empty query string is rejected (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.validate_query("")


def test_validate_query_whitespace_only(service):
    """Verify whitespace-only query is rejected (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.validate_query("   \t \n  ")


def test_validate_query_none(service):
    """Verify None query is rejected (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.validate_query(None)  # type: ignore


def test_search_by_name_rejects_empty_query(service):
    """Verify search_by_name rejects empty query (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.search_by_name("")


def test_search_by_email_rejects_whitespace_query(service):
    """Verify search_by_email rejects whitespace query (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.search_by_email("   ")


def test_search_unified_rejects_empty_query(service):
    """Verify search rejects empty query (VR-01, AC-03)."""
    with pytest.raises(ValidationError, match="Invalid Input"):
        service.search("")


def test_cli_empty_name_error_output(capsys):
    """Verify CLI outputs ERROR: Invalid Input when --name is empty (EH-01, AC-03)."""
    exit_code = main(["--name", ""])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out.strip() == "ERROR: Invalid Input"


def test_cli_whitespace_email_error_output(capsys):
    """Verify CLI outputs ERROR: Invalid Input when --email is whitespace (EH-01, AC-03)."""
    exit_code = main(["--email", "   "])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out.strip() == "ERROR: Invalid Input"


def test_cli_whitespace_query_error_output(capsys):
    """Verify CLI outputs ERROR: Invalid Input when --query is whitespace (EH-01, AC-03)."""
    exit_code = main(["--query", "  \t "])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out.strip() == "ERROR: Invalid Input"


# ============================================================================
# VR-02, EH-02: Command-line argument validation
# ============================================================================

def test_cli_no_arguments_shows_instructions(capsys):
    """Verify CLI prints help instructions and exits when search flags omitted (VR-02, EH-02)."""
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "usage:" in captured.out or "Search customer records" in captured.out


def test_cli_file_flag_only_shows_instructions(capsys):
    """Verify CLI prints help when only --file is given without search terms (VR-02, EH-02)."""
    exit_code = main(["--file", "customers.json"])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "usage:" in captured.out or "Search customer records" in captured.out


def test_cli_invalid_flag_exits_with_error(capsys):
    """Verify CLI exits and displays usage when an unknown flag is provided (EH-02)."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--unknown-option"])
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err or "usage:" in captured.err


def test_cli_mutually_exclusive_flags_rejected(capsys):
    """Verify CLI rejects passing both --name and --email (EH-02)."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--name", "Alice", "--email", "alice@example.com"])
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "not allowed with argument" in captured.err


# ============================================================================
# EH-03, AC-05: No matches messaging
# ============================================================================

def test_cli_no_matches_by_name(capsys):
    """Verify message output when name query has no matches (EH-03, AC-05)."""
    exit_code = main(["--name", "UnknownPerson"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "MESSAGE: No customers found that matched UnknownPerson"


def test_cli_no_matches_by_email(capsys):
    """Verify message output when email query has no matches (EH-03, AC-05)."""
    exit_code = main(["--email", "nobody@nowhere.com"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "MESSAGE: No customers found that matched nobody@nowhere.com"


def test_cli_no_matches_unified_query(capsys):
    """Verify message output when unified query has no matches (EH-03, AC-05)."""
    exit_code = main(["--query", "xyz999"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "MESSAGE: No customers found that matched xyz999"


# ============================================================================
# EH-04: Graceful storage error handling in CLI
# ============================================================================

def test_cli_missing_storage_file_handled_gracefully(capsys):
    """Verify missing JSON file outputs clear error message without stack trace (EH-04)."""
    exit_code = main(["--file", "nonexistent_file.json", "--name", "Alice"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ERROR: Failed to load customer records" in captured.out
