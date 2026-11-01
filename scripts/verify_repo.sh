
#!/usr/bin/env bash
set -euo pipefail

# Repository verification for the Customer Search CLI.
# Run from any directory with: ./scripts/verify_repo.sh

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

fail() {
    echo "FAIL: $*" >&2
    exit 1
}

pass() {
    echo "PASS: $*"
}

echo "[1/4] Checking required repository files"

for file in \
    AGENTS.md \
    REQUIREMENTS.md \
    SPEC.md \
    ARCHITECTURE.md \
    TASKS.md \
    README.md \
    docs/traceability.md \
    src/cli.py \
    customers.json
do
    [[ -f "$file" ]] || fail "Required file is missing: $file"
done

[[ -d tests ]] || fail "Tests directory is missing"
pass "Required files and tests directory exist"

echo "[2/4] Running automated tests"

python -m pytest -v

pass "Automated tests passed"


echo "[3/4] Checking test traceability"

TRACEABILITY="docs/traceability.md"

[[ -f "$TRACEABILITY" ]] || fail "Missing $TRACEABILITY"

TEST_LIST="$(mktemp)"
trap 'rm -f "$TEST_LIST"' EXIT

python -m pytest --collect-only -q > "$TEST_LIST" \
    || fail "Could not collect tests with pytest"

test_count=0
missing_count=0

while IFS= read -r test_id; do
    # Skip empty lines and pytest summary lines.
    [[ -z "$test_id" ]] && continue
    [[ "$test_id" == *" tests collected"* ]] && continue
    [[ "$test_id" == *" test collected"* ]] && continue

    test_file="${test_id%%::*}"

    # Ignore lines that are not pytest test IDs.
    [[ "$test_file" == *".py" ]] || continue

    test_count=$((test_count + 1))

    if ! grep -Fq "$test_file" "$TRACEABILITY"; then
        echo "  MISSING: $test_id" >&2
        missing_count=$((missing_count + 1))
    fi
done < "$TEST_LIST"

(( test_count > 0 )) || fail "No test cases were collected"

if (( missing_count > 0 )); then
    echo >&2
    echo "FAIL: $missing_count of $test_count tests belong to files not referenced in $TRACEABILITY:" >&2
    fail "Update $TRACEABILITY to include the missing test files listed above"
fi

pass "All $test_count collected tests belong to files referenced in $TRACEABILITY"


echo "[4/4] Checking CLI documentation"

python - <<'PY'
import re
import sys
from pathlib import Path

source = Path("src/cli.py").read_text(encoding="utf-8")
readme = Path("README.md").read_text(encoding="utf-8")

# Extract long-form CLI options declared through argparse.
options = set(
    re.findall(
        r"""add_argument\(\s*["'](--[a-zA-Z0-9-]+)""",
        source,
    )
)

if not options:
    print("FAIL: No CLI options found in src/cli.py", file=sys.stderr)
    sys.exit(1)

missing = sorted(option for option in options if option not in readme)

if missing:
    print(
        "FAIL: CLI options missing from README.md: "
        + ", ".join(missing),
        file=sys.stderr,
    )
    sys.exit(1)

print("PASS: All declared CLI options are documented in README.md")
PY

echo "VERIFY_REPO: PASS"
