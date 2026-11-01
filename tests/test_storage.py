"""Tests for domain model and storage loader (T-02)."""
import json
import pytest
from pathlib import Path

from src.models import Customer
from src.storage import StorageError, load_customers


def test_customer_model_instantiation():
    """Verify Customer model instantiates with valid data."""
    customer = Customer(id=1, name="Alice Smith", email="alice@example.com")
    assert customer.id == 1
    assert customer.name == "Alice Smith"
    assert customer.email == "alice@example.com"
    assert customer["name"] == "Alice Smith"
    assert customer.to_dict() == {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice@example.com",
    }


def test_customer_model_validation():
    """Verify Customer model validates attribute types."""
    with pytest.raises(ValueError, match="id"):
        Customer(id="not-an-int", name="Alice", email="alice@example.com")  # type: ignore

    with pytest.raises(ValueError, match="id"):
        Customer(id=True, name="Alice", email="alice@example.com")  # bool is subclass of int

    with pytest.raises(ValueError, match="name"):
        Customer(id=1, name=123, email="alice@example.com")  # type: ignore

    with pytest.raises(ValueError, match="email"):
        Customer(id=1, name="Alice", email=456)  # type: ignore


def test_customer_from_dict_validation():
    """Verify Customer.from_dict checks missing fields and input format."""
    with pytest.raises(ValueError, match="must be a dictionary"):
        Customer.from_dict("invalid")  # type: ignore

    with pytest.raises(ValueError, match="Missing required field: 'email'"):
        Customer.from_dict({"id": 1, "name": "Alice"})


def test_load_customers_default_file():
    """Verify load_customers loads customers.json successfully (AC-07, C-04)."""
    customers = load_customers()
    assert isinstance(customers, list)
    assert len(customers) >= 3
    first = customers[0]
    assert first["id"] == 1
    assert first["name"] == "Alice Smith"
    assert first["email"] == "alice@example.com"


def test_load_customers_custom_file(tmp_path: Path):
    """Verify load_customers works with a custom file path."""
    test_file = tmp_path / "custom.json"
    sample_data = [{"id": 10, "name": "Test User", "email": "test@test.com"}]
    test_file.write_text(json.dumps(sample_data), encoding="utf-8")

    customers = load_customers(str(test_file))
    assert len(customers) == 1
    assert customers[0]["name"] == "Test User"


def test_load_customers_missing_file():
    """Verify load_customers raises StorageError on missing file (EH-04)."""
    with pytest.raises(StorageError) as exc_info:
        load_customers("non_existent_file.json")
    assert "Failed to load customer records" in str(exc_info.value)
    assert "not found" in str(exc_info.value)


def test_load_customers_malformed_json(tmp_path: Path):
    """Verify load_customers raises StorageError on malformed JSON (EH-04)."""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{ unquoted_key: 123 ", encoding="utf-8")

    with pytest.raises(StorageError) as exc_info:
        load_customers(str(bad_file))
    assert "Failed to load customer records" in str(exc_info.value)
    assert "malformed JSON" in str(exc_info.value)


def test_load_customers_root_not_list(tmp_path: Path):
    """Verify load_customers raises StorageError when root is not a list (VR-03, EH-04)."""
    dict_file = tmp_path / "dict.json"
    dict_file.write_text(json.dumps({"id": 1, "name": "Alice", "email": "a@b.com"}), encoding="utf-8")

    with pytest.raises(StorageError) as exc_info:
        load_customers(str(dict_file))
    assert "Failed to load customer records" in str(exc_info.value)
    assert "must be a list" in str(exc_info.value)


def test_load_customers_record_missing_required_fields(tmp_path: Path):
    """Verify load_customers raises StorageError when records lack fields (VR-03, EH-04)."""
    incomplete_file = tmp_path / "incomplete.json"
    incomplete_file.write_text(json.dumps([{"id": 1, "name": "No Email"}]), encoding="utf-8")

    with pytest.raises(StorageError) as exc_info:
        load_customers(str(incomplete_file))
    assert "Failed to load customer records" in str(exc_info.value)
    assert "Missing required field" in str(exc_info.value)


def test_load_customers_record_invalid_field_type(tmp_path: Path):
    """Verify load_customers raises StorageError when record field types are wrong (VR-03, EH-04)."""
    invalid_file = tmp_path / "invalid_type.json"
    invalid_file.write_text(json.dumps([{"id": "one", "name": "Alice", "email": "a@b.com"}]), encoding="utf-8")

    with pytest.raises(StorageError) as exc_info:
        load_customers(str(invalid_file))
    assert "Failed to load customer records" in str(exc_info.value)
    assert "must be an integer" in str(exc_info.value)
