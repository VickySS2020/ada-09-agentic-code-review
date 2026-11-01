# Change Request
Change ID: CR-01

## Goal
Strengthen customer record validation so that records with an empty or whitespace-only name or email are rejected.
The validation must apply both when creating a Customer instance and when loading customer records from a JSON file.

Invalid records must be handled through the existing storage error-handling mechanism, producing a readable error rather than an unhandled exception.

## Requirements Covered
- FR-07
- VR-03
- AC-07

## Constraints
- Follow AGENTS.md.
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Preserve architecture boundaries.
- Do not weaken existing tests.
- Modify only the necessary application and test files.
- Do not introduce email-format validation or unrelated business rules.
- Preserve the behavior of existing valid customer records.

## Verification
The change is complete when the following observable evidence is available:
1. Unit tests confirm that empty and whitespace-only names are rejected.
2. Unit tests confirm that empty and whitespace-only email addresses are rejected.
3. Existing tests confirm that valid customer records are still accepted.
4. Storage tests confirm that invalid records raise StorageError with a useful error message.
5. CLI tests confirm that invalid customer data produces a readable error without an unhandled traceback.
6. The complete test suite passes using: 
```bash
./scripts/verify_repo.sh
```

## Human Approval
Approved to implement: YES
Approved by: Victoria Saavedra Sánchez
Date: 01/11/2026
