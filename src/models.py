"""Customer domain model."""
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Customer:
    """Represents a customer record."""
    id: int
    name: str
    email: str

    def __post_init__(self) -> None:
        if not isinstance(self.id, int) or isinstance(self.id, bool):
            raise ValueError("Customer 'id' must be an integer")
        if not isinstance(self.name, str):
            raise ValueError("Customer 'name' must be a string")
        if not isinstance(self.email, str):
            raise ValueError("Customer 'email' must be a string")

    def to_dict(self) -> dict[str, Any]:
        """Convert Customer instance to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Customer":
        """Create Customer instance from dictionary with validation."""
        if not isinstance(data, dict):
            raise ValueError("Customer record must be a dictionary")
        for field in ("id", "name", "email"):
            if field not in data:
                raise ValueError(f"Missing required field: '{field}'")
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def __getitem__(self, item: str) -> Any:
        """Allow dictionary-style attribute access."""
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)
