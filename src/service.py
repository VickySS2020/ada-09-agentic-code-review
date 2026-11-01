"""Customer search service layer."""
from typing import Any, Callable

from src.storage import load_customers


class ValidationError(ValueError):
    """Raised when query input fails validation rules (VR-01)."""
    pass


class CustomerService:
    """Service handling business logic for customer search and query validation."""

    def __init__(
        self,
        file_path: str = "customers.json",
        customers: list[dict[str, Any]] | None = None,
        loader: Callable[[str], list[dict[str, Any]]] = load_customers,
    ) -> None:
        self.file_path = file_path
        self._loader = loader
        self._customers = customers

    def get_customers(self) -> list[dict[str, Any]]:
        """Retrieve customer dataset, loading from storage if not cached."""
        if self._customers is None:
            self._customers = self._loader(self.file_path)
        return self._customers

    def validate_query(self, query: str) -> str:
        """Validate and sanitize a search query.

        Args:
            query: The raw query string.

        Returns:
            Sanitized query string with leading and trailing whitespace stripped.

        Raises:
            ValidationError: If query is empty or whitespace-only (VR-01).
        """
        if query is None or not query.strip():
            raise ValidationError("Invalid Input")
        return query.strip()

    def search_by_name(self, query: str) -> list[dict[str, Any]]:
        """Search customer records by name with case-insensitive partial matching.

        Args:
            query: Name query term.

        Returns:
            List of customer records matching the name term.
        """
        term = self.validate_query(query).lower()
        return [
            record
            for record in self.get_customers()
            if term in str(record.get("name", "")).lower()
        ]

    def search_by_email(self, query: str) -> list[dict[str, Any]]:
        """Search customer records by email with case-insensitive partial matching.

        Args:
            query: Email query term.

        Returns:
            List of customer records matching the email term.
        """
        term = self.validate_query(query).lower()
        return [
            record
            for record in self.get_customers()
            if term in str(record.get("email", "")).lower()
        ]

    def search(self, query: str) -> list[dict[str, Any]]:
        """Unified search across customer names and emails.

        Args:
            query: Search query term.

        Returns:
            List of customer records whose name or email matches the term.
        """
        term = self.validate_query(query).lower()
        return [
            record
            for record in self.get_customers()
            if term in str(record.get("name", "")).lower()
            or term in str(record.get("email", "")).lower()
        ]
