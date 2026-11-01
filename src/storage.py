"""Storage layer for loading customer data from local JSON file."""
import json
from pathlib import Path
from typing import Any

from src.models import Customer


class StorageError(Exception):
    """Raised when customer data cannot be loaded or parsed."""
    pass


def load_customers(file_path: str = "customers.json") -> list[dict[str, Any]]:
    """Load customer records from a local JSON file.

    Args:
        file_path: Path to the JSON file (defaults to 'customers.json').

    Returns:
        A list of dictionaries representing customer records.

    Raises:
        StorageError: If the file is missing, inaccessible, malformed, or invalid.
    """
    path = Path(file_path)
    if not path.is_file():
        raise StorageError(f"Failed to load customer records: file '{file_path}' not found")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise StorageError(f"Failed to load customer records: malformed JSON ({exc.msg})") from exc
    except OSError as exc:
        raise StorageError(f"Failed to load customer records: cannot read file ({exc})") from exc

    if not isinstance(data, list):
        raise StorageError("Failed to load customer records: root JSON element must be a list")

    customers: list[dict[str, Any]] = []
    for index, record in enumerate(data):
        try:
            customer = Customer.from_dict(record)
            customers.append(customer.to_dict())
        except (ValueError, TypeError) as exc:
            raise StorageError(
                f"Failed to load customer records: invalid record at index {index} ({exc})"
            ) from exc

    return customers
