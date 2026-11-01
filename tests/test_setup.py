"""Test environment and project setup for T-01."""
import json
import sys
from pathlib import Path


def test_python_version():
    """Verify environment satisfies Python 3.11+ compatibility (NFR-05, C-01)."""
    assert sys.version_info >= (3, 11), f"Expected Python 3.11+, got {sys.version}"


def test_customers_json_exists_and_valid():
    """Verify customers.json exists and is valid JSON matching schema (VR-03, C-04)."""
    file_path = Path("customers.json")
    assert file_path.is_file(), "customers.json must exist in project root"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), "customers.json root must be a list"
    assert len(data) > 0, "customers.json should contain initial records"

    for record in data:
        assert isinstance(record, dict), "Each customer record must be an object"
        assert "id" in record and isinstance(record["id"], int)
        assert "name" in record and isinstance(record["name"], str)
        assert "email" in record and isinstance(record["email"], str)


def test_project_structure():
    """Verify project structure contains src and tests directories."""
    src_dir = Path("src")
    tests_dir = Path("tests")
    assert src_dir.is_dir(), "src directory must exist"
    assert tests_dir.is_dir(), "tests directory must exist"
    assert (src_dir / "__init__.py").is_file(), "src/__init__.py must exist"
    assert (tests_dir / "__init__.py").is_file(), "tests/__init__.py must exist"
