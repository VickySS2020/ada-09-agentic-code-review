"""Automated tests for --sort CLI argument (CR-01: FR-04, FR-06, AC-04)."""
import pytest
from src.cli import main


@pytest.fixture
def sample_customers():
    return [
        {"id": 1, "name": "Charlie Brown", "email": "charlie@domain.com"},
        {"id": 2, "name": "Alice Smith", "email": "alice@example.com"},
        {"id": 3, "name": "Bob Jones", "email": "bob@example.com"},
        {"id": 4, "name": "Alice Wonderland", "email": "alice.wonder@domain.org"},
    ]


# ---------------------------------------------------------------------------
# --sort name
# ---------------------------------------------------------------------------

def test_sort_by_name_ascending(capsys):
    """--sort name returns records in case-insensitive alphabetical order by name."""
    exit_code = main(["--email", "example", "--sort", "name"])
    captured = capsys.readouterr()
    assert exit_code == 0
    output = captured.out
    # Alice should appear before Bob in the output
    assert output.index("Alice Smith") < output.index("Bob Jones")


def test_sort_by_name_case_insensitive(capsys):
    """--sort name ordering is case-insensitive."""
    # Use --query so both "alice" (lowercase name) and uppercase records match
    exit_code = main(["--query", "example", "--sort", "name"])
    captured = capsys.readouterr()
    assert exit_code == 0
    lines = captured.out.splitlines()
    # Collect name values from data rows (skip separator and header lines)
    names = [
        line.split("|")[2].strip()
        for line in lines
        if "|" in line and "Name" not in line and "+-" not in line
    ]
    lower_names = [n.lower() for n in names]
    assert lower_names == sorted(lower_names), (
        f"Names not in case-insensitive alphabetical order: {names}"
    )


def test_sort_by_name_retains_all_matches(capsys):
    """--sort name does not drop or add records; match set is unchanged."""
    exit_code_unsorted = main(["--email", "example"])
    out_unsorted = capsys.readouterr().out

    exit_code_sorted = main(["--email", "example", "--sort", "name"])
    out_sorted = capsys.readouterr().out

    assert exit_code_unsorted == exit_code_sorted == 0
    # Same customers present regardless of order
    assert "Alice Smith" in out_sorted
    assert "Bob Jones" in out_sorted
    assert out_sorted.count("Alice Smith") == out_unsorted.count("Alice Smith")
    assert out_sorted.count("Bob Jones") == out_unsorted.count("Bob Jones")


# ---------------------------------------------------------------------------
# --sort email
# ---------------------------------------------------------------------------

def test_sort_by_email_ascending(capsys):
    """--sort email returns records in case-insensitive alphabetical order by email."""
    exit_code = main(["--email", "example", "--sort", "email"])
    captured = capsys.readouterr()
    assert exit_code == 0
    output = captured.out
    # alice@example.com comes before bob@example.com alphabetically
    assert output.index("alice@example.com") < output.index("bob@example.com")


def test_sort_by_email_case_insensitive(capsys):
    """--sort email ordering is case-insensitive."""
    exit_code = main(["--query", "example", "--sort", "email"])
    captured = capsys.readouterr()
    assert exit_code == 0
    lines = captured.out.splitlines()
    emails = [
        line.split("|")[3].strip()
        for line in lines
        if "|" in line and "Email" not in line and "+-" not in line
    ]
    lower_emails = [e.lower() for e in emails]
    assert lower_emails == sorted(lower_emails), (
        f"Emails not in case-insensitive alphabetical order: {emails}"
    )


def test_sort_by_email_retains_all_matches(capsys):
    """--sort email does not drop or add records; match set is unchanged."""
    exit_code_unsorted = main(["--email", "example"])
    out_unsorted = capsys.readouterr().out

    exit_code_sorted = main(["--email", "example", "--sort", "email"])
    out_sorted = capsys.readouterr().out

    assert exit_code_unsorted == exit_code_sorted == 0
    assert "alice@example.com" in out_sorted
    assert "bob@example.com" in out_sorted
    assert out_sorted.count("alice@example.com") == out_unsorted.count("alice@example.com")
    assert out_sorted.count("bob@example.com") == out_unsorted.count("bob@example.com")


# ---------------------------------------------------------------------------
# Output format with --sort
# ---------------------------------------------------------------------------

def test_sort_output_retains_id_name_email_columns(capsys):
    """Table columns ID, Name, Email are present when --sort is used (AC-04)."""
    exit_code = main(["--name", "Alice", "--sort", "name"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "| ID " in captured.out
    assert "| Name " in captured.out
    assert "| Email " in captured.out


# ---------------------------------------------------------------------------
# Regression: searches without --sort continue to work
# ---------------------------------------------------------------------------

def test_no_sort_search_by_name_unchanged(capsys):
    """Existing --name search without --sort still works as before."""
    exit_code = main(["--name", "Alice"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Alice Smith" in captured.out
    assert "| ID " in captured.out


def test_no_sort_search_by_email_unchanged(capsys):
    """Existing --email search without --sort still works as before."""
    exit_code = main(["--email", "bob@example.com"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Bob Jones" in captured.out


def test_no_sort_unified_query_unchanged(capsys):
    """Existing --query search without --sort still works as before."""
    exit_code = main(["--query", "charlie"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Charlie Brown" in captured.out
    assert "charlie@domain.com" in captured.out


def test_no_sort_no_matches_message_unchanged(capsys):
    """No-match message is unchanged when --sort is omitted."""
    exit_code = main(["--name", "NobodyHere"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "MESSAGE: No customers found that matched NobodyHere"


def test_sort_no_matches_still_shows_message(capsys):
    """When sort is supplied but no records match, the no-match message is shown."""
    exit_code = main(["--name", "NobodyHere", "--sort", "name"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "MESSAGE: No customers found that matched NobodyHere" in captured.out.strip()


def test_invalid_sort_value_exits_with_error(capsys):
    """An unsupported --sort value is rejected by argparse."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--name", "Alice", "--sort", "invalid"])
    assert exc_info.value.code != 0
