# PR Evidence
## Change
Change ID: CR-01

PR / Branch: CR-01 implementation #1 / ada09/cr-01

Base commit: initial commit - (26edccc)

Final commit: 4135180 fix: address ADA-09 review findings

## Requirements / Acceptance Criteria
- FR-07
- VR-03
- AC-07

## Implementation
Coder report: `results/coder-report.md`

The Coder Agent implemented CR-01 by adding validation to reject empty or whitespace-only customer names and emails. It added tests to verify model validation, storage error handling, and acceptance of valid records. The test suite increased from 62 to 72 passing tests after addressing review feedback.

The implementation preserved the existing three-tier architecture and addressed additional review findings, including CLI error handling, repository hygiene, and test traceability. All reported checks passed, although the Bash verification script could not be executed directly in the Windows environment. 

Files changed: 
- `src/models.py`
- `tests/test_storage.py`
- `docs/traceability.md`
- `tests/test_cli.py`

Commits:
1. 4135180 fix: address ADA-09 review findings
2. d9fe562 build: untrack __pycache__ and add root .gitignore
3. 992bfc5 fix test traceability
4. 71ef520 feat: implement CR-01

## Verification
Verification command: 
```bash
./scripts/verify_repo.sh
```
Final result:
```
PASS: Required files and tests directory exist. 
PASS: Automated tests passed. 
PASS: All 72 collected tests belong to files referenced in docs/traceability.md. 
PASS: All declared CLI options are documented in README.md. 
VERIFY_REPO: PASS
```
Tests:
```
================= 72 passed in 0.69s =================
```

## Independent Review
Review report: `review-report.md`

The Independent Reviewer evaluated CR-01 against the functional requirements, acceptance criteria, architecture constraints, and automated tests. It identified one MUST FIX finding: the absence of a CLI test verifying that invalid customer records produce readable errors without unhandled tracebacks. It also identified three SHOULD FIX findings involving committed Python bytecode, inaccurate verification evidence, and incomplete test traceability; and one OPTIONAL architectural improvement concerning in-memory customer records bypassing domain validation.

MUST FIX found: 1
  - RF-01: Missing automated CLI test for invalid customer data (CR-01 Verification Item #5).

SHOULD FIX found: 3
  - RF-02: Committed Python bytecode (`.pyc`) files and missing `.gitignore`.
  - RF-03: Inaccurate verification evidence and environment metadata in `verification-report.md`.
  - RF-04: Incomplete CR-01 entries in `docs/traceability.md`.

OPTIONAL found: 1
  - RF-05: In-memory customer injection in `CustomerService` bypasses domain model validation.

## Human Decisions
Accepted: 2 (**RF-01**, **RF-02**)

Modified: 1 (**RF-04**)

Rejected: 2 (**RF-03**, **RF-05**)

Deferred: 0

## Re-review
Resolved: 3 (**RF-01**, **RF-02**, **RF-04**)

Partially resolved: 0

Not resolved: 0

New MUST FIX: 0

## Traceability
| Requirement / AC | Task / Change | Code | Test | Review Finding |
|---|---|---|---|---|
|FR-07|CR-01|--|`tests/test_storage.py`, `tests/test_cli.py`|**RF-04**|
|AC-07|CR-01|`src/models.py`|`tests/test_storage.py`, `tests/test_cli.py`|**RF-01**|

## Remaining Risks / Technical Debt
There were no risks or regressions found.

## Final Human Decision
[ ] NOT READY

[X] READY FOR HUMAN MERGE

Approved by: Victoria Saavedra Sánchez 

Date: 2026/11/02