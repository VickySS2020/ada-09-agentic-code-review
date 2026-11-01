"""Unit tests for CustomerService business logic (T-03)."""
import time
import pytest
from src.service import CustomerService


@pytest.fixture
def sample_customers():
    return [
        {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Jones", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie Brown", "email": "charlie@domain.com"},
        {"id": 4, "name": "Alice Wonderland", "email": "alice.wonder@domain.org"},
    ]


@pytest.fixture
def service(sample_customers):
    return CustomerService(customers=sample_customers)


def test_search_by_name_exact_and_partial(service):
    """Verify search by name supports case-insensitive partial matching (AC-01, SR-01)."""
    # Exact prefix
    results = service.search_by_name("Alice")
    assert len(results) == 2
    assert {r["name"] for r in results} == {"Alice Smith", "Alice Wonderland"}

    # Lowercase partial substring
    results_partial = service.search_by_name("ali")
    assert len(results_partial) == 2

    # Uppercase partial substring
    results_upper = service.search_by_name("SMITH")
    assert len(results_upper) == 1
    assert results_upper[0]["name"] == "Alice Smith"


def test_search_by_email_exact_and_partial(service):
    """Verify search by email supports case-insensitive partial matching (AC-02, SR-02)."""
    # Partial domain matching
    results = service.search_by_email("example.com")
    assert len(results) == 2
    assert {r["id"] for r in results} == {1, 2}

    # Partial local part matching
    results_local = service.search_by_email("alice@")
    assert len(results_local) == 1
    assert results_local[0]["email"] == "alice@example.com"

    # Case insensitivity
    results_case = service.search_by_email("DOMAIN.ORG")
    assert len(results_case) == 1
    assert results_case[0]["id"] == 4


def test_search_unified_query(service):
    """Verify unified search matches name OR email (AC-06, SR-03)."""
    # Match in name only
    results_name = service.search("Brown")
    assert len(results_name) == 1
    assert results_name[0]["name"] == "Charlie Brown"

    # Match in email only
    results_email = service.search("domain.org")
    assert len(results_email) == 1
    assert results_email[0]["name"] == "Alice Wonderland"

    # Match across both name and email
    results_both = service.search("alice")
    assert len(results_both) == 2


def test_search_no_matches(service):
    """Verify search returns empty list when no customer matches."""
    assert service.search_by_name("NonExistent") == []
    assert service.search_by_email("notfound@nowhere.com") == []
    assert service.search("Unknown") == []


def test_search_query_whitespace_handling(service):
    """Verify leading and trailing whitespace is trimmed before searching."""
    results = service.search_by_name("   Alice   ")
    assert len(results) == 2


def test_search_performance_sub_100ms():
    """Verify search operations execute under 100 milliseconds (AC-08, NFR-04)."""
    # Generate larger customer dataset (1000 items)
    large_dataset = [
        {"id": i, "name": f"Customer {i}", "email": f"customer_{i}@test.com"}
        for i in range(1000)
    ]
    service = CustomerService(customers=large_dataset)

    start_time = time.perf_counter()
    results = service.search("500")
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    assert len(results) >= 1
    assert elapsed_ms < 100.0, f"Search took {elapsed_ms:.2f} ms, expected < 100 ms"


def test_business_logic_separation_from_presentation(service):
    """Verify service returns pure data structures without presentation code (NFR-02)."""
    results = service.search_by_name("Alice")
    assert isinstance(results, list)
    for item in results:
        assert isinstance(item, dict)
        assert "id" in item
        assert "name" in item
        assert "email" in item
