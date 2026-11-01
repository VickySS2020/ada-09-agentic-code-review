
#!/usr/bin/env python3
"""Check that the repository contains its essential contract files."""

from pathlib import Path
import sys


# Resolve the repository root from this script's location,
# so the check works regardless of the current working directory.
REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
]


def main() -> int:
    missing = [
        relative_path
        for relative_path in REQUIRED_FILES
        if not (REPO_ROOT / relative_path).is_file()
    ]

    if missing:
        print("REPO_CONTRACT: FAIL")
        for relative_path in missing:
            print(f"Missing: {relative_path}")
        return 1

    print("REPO_CONTRACT: PASS")
    print(f"All {len(REQUIRED_FILES)} required files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
