"""Command-line interface for customer search."""
import argparse
import sys
from pathlib import Path
from typing import Any, Sequence

# Ensure project root is in sys.path when executed as a script
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.service import CustomerService
from src.storage import StorageError


def format_table(records: list[dict[str, Any]]) -> str:
    """Format customer records as a readable table with ID, Name, Email columns.

    Args:
        records: List of customer dictionaries.

    Returns:
        Formatted ASCII table string.
    """
    if not records:
        return ""

    headers = ["ID", "Name", "Email"]
    id_width = max(len(headers[0]), max(len(str(r.get("id", ""))) for r in records))
    name_width = max(len(headers[1]), max(len(str(r.get("name", ""))) for r in records))
    email_width = max(len(headers[2]), max(len(str(r.get("email", ""))) for r in records))

    separator = f"+-{'-' * id_width}-+-{'-' * name_width}-+-{'-' * email_width}-+"
    header_line = (
        f"| {headers[0].ljust(id_width)} | {headers[1].ljust(name_width)} | {headers[2].ljust(email_width)} |"
    )

    lines = [separator, header_line, separator]
    for record in records:
        line = (
            f"| {str(record.get('id', '')).ljust(id_width)} "
            f"| {str(record.get('name', '')).ljust(name_width)} "
            f"| {str(record.get('email', '')).ljust(email_width)} |"
        )
        lines.append(line)
    lines.append(separator)

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Construct command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="customer_search",
        description="Search customer records by name or email.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--name",
        type=str,
        help="Search customers by name (case-insensitive substring)",
    )
    group.add_argument(
        "--email",
        type=str,
        help="Search customers by email (case-insensitive substring)",
    )
    group.add_argument(
        "--query",
        type=str,
        help="Search customers by name or email (case-insensitive substring)",
    )
    parser.add_argument(
        "--file",
        type=str,
        default="customers.json",
        help="Path to customer JSON data file (default: customers.json)",
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=["name", "email"],
        default=None,
        help="Sort matching records alphabetically by 'name' or 'email' (case-insensitive)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Execute customer search CLI.

    Args:
        argv: Optional sequence of argument strings (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    # Check if any search argument was provided
    if args.name is None and args.email is None and args.query is None:
        parser.print_help()
        return 2

    service = CustomerService(file_path=args.file)

    try:
        if args.name is not None:
            query = args.name
            results = service.search_by_name(query)
        elif args.email is not None:
            query = args.email
            results = service.search_by_email(query)
        else:
            query = args.query
            results = service.search(query)
    except ValueError:
        print("ERROR: Invalid Input")
        return 1
    except StorageError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.sort is not None:
        sort_key = args.sort
        results = sorted(results, key=lambda r: str(r.get(sort_key, "")).lower())

    if not results:
        print(f"MESSAGE: No customers found that matched {query.strip()}")
        return 0

    table = format_table(results)
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
