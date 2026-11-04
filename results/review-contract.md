# Review Contract

## Change
CR-01

## Requirements / Acceptance Criteria
- FR-07
- VR-03
- AC-07

## Architecture Constraints
- Expected dependency flow: CLI Layer (src/cli.py) → Customer Service Layer (src/service.py) → Storage Layer (src/storage.py). 

    The Customer model (src/models.py) defines and validates customer data independently. Dependencies must not flow backward, and business logic must remain independent of CLI presentation.

- Business-rule location: Required customer attribute validation (non-empty, non-whitespace name and email) must reside in the Customer model (src/models.py). 

    JSON structure and record-loading validation must remain in the Storage Layer (src/storage.py). 
    
    The CLI (src/cli.py) is responsible only for displaying readable errors.

- Protected boundaries:
    - Preserve the three-layer architecture and separation of responsibilities.
    - Do not move business validation into the CLI or storage presentation logic.
    - Preserve the existing StorageError mechanism for invalid customer records loaded from JSON.
    - Maintain compatibility with existing valid customer records and the JSON schema (id, name, email).
    - Do not introduce email-format validation, external dependencies, APIs, or unrelated business rules.
    - Do not modify existing requirements or acceptance criteria to accommodate implementation changes.

## Review Rules
- Verify requirement coverage.
- Check architecture boundaries.
- Inspect tests for masking / false confidence.
- Check regression behavior.
- Identify unnecessary technical debt.
- Cite evidence for every finding.

## Severity
MUST FIX:
Requirement violation, regression, security/integrity risk,
hallucinated API/dependency, broken architecture constraint,
or defect that makes the change unsafe to approve.

SHOULD FIX:
Significant maintainability, coverage, design, or clarity issue
that does not block the requested behavior.

OPTIONAL:
Non-blocking improvement outside the minimum acceptance threshold.
