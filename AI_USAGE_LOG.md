# AI Usage Log

## Entry 01 - Initial Repository Change

Stage: Change Request Definition

Prompt/goal: Review the branch 'after' of the repository, and propose a small but sufficient change that requires review. Don't propose changes like this:
- Format or comment changes.
- A task without verifiable criteria.
- A change so big it can't be reviewed in a single session.
- A new feature that requires redesigning the whole architecture.

AI contribution: The agent reviewed the repository documentation, source structure, and tests. It suggested changing verify_repo.sh, and also suggested adding a validation rule that verifies that customer records with an empty or whitespace-only name or email are NOT accepted.

Student decision:  
I reviewed the findings against the repository files and confirmed that `model.py` only checks that the "name" or "email" attribute is a string, it does not deal with empty or whitespace-only values. I rejected the other proposal, since it was directed at a vital document of our agent-ready repository that is outside this project's scope.

Impact:
CHANGE_REQUEST.md

## Entry 02 - Implementation Plan

Stage: CR Implementation

Prompt/goal: Implement the approved change described in CHANGE_REQUEST.md.
Before implementation:
1. Read AGENTS.md.
2. Read the referenced requirements and acceptance criteria.
3. Read SPEC.md and ARCHITECTURE.md.
4. Inspect the relevant code and tests.
5. Produce a short implementation plan.

AI contribution: The coding agent analyzed the change requirements and existing repository, confirming a baseline of 62 passing tests. It implemented domain-level validation in src/models.py to reject empty or whitespace-only customer names and emails, leveraging existing storage error handling to report invalid records clearly. It expanded the test suite to cover invalid and valid customer records, then performed verification through automated tests, traceability checks, CLI documentation review, and required repository file checks.

Student decision: The implementation plan was reviewed and approved.

Impact: results/coder-report.md

## Entry 03 - Coder-Agent Implementation

Stage: CR Implementation

Prompt/goal: Implement the approved change described in CHANGE_REQUEST.md.
Implementation rules:
- Keep the change scoped to the approved Change Request.
- Respect existing architecture boundaries.
- Do not invent APIs or dependencies.
- Do not weaken or remove existing tests.
- Add or update tests for the requested behavior.
- Do not modify REQUIREMENTS.md or SPEC.md merely to make the code fit.

When finished:
- run the repository verification command,
- report files changed,
- report commands executed,
- report tests added/updated,
- report any assumptions or limitations,
- create results/coder-report.md.

Do not review or approve your own change.

AI contribution: The coder agent implemented the plan, first editing `src/model.py` to include 2 blank-value guards for 'name' and 'email' respectably and adding 9 new test cases in `tests/test_storage.py`.

Student decision:  The changes were accepted, but it was noted during the first human-review (`results/verification-report.md`) that the agent neither executed `./script/verify_repo.sh` with the provided script nor edited the tracebility matrix with the new tests. This last problem was informed to the coder agent so it could be fixed before evaluation by the reviewer agent.

Impact: results/coder-report.md, src/model.py, tests/test_storage.py, results/verification-report.md

## Entry 04 - Reviewer-Agent Audit

Stage: Implementation Review

Prompt/goal: Act as an independent reviewer for the PR candidate in the repository (PR #1 - CR-01 implementation) and report any finding as MUST FIX, SHOULD FIX, or OPTIONAL citing concrete evidence for each one.

AI contribution: The Independent Reviewer evaluated CR-01 against the functional requirements, acceptance criteria, architecture constraints, and automated tests. It identified one MUST FIX finding: the absence of a CLI test verifying that invalid customer records produce readable errors without unhandled tracebacks. It also identified three SHOULD FIX findings involving committed Python bytecode, inaccurate verification evidence, and incomplete test traceability; and one OPTIONAL architectural improvement concerning in-memory customer records bypassing domain validation.

Student decision: Each finding was reviewed and 3 out 5 of the findings were accepted/modified (**RF-01**, **RF-02**, **RF-04**) and 2 were rejected (**RF-03**, **RF-05**).

Impact: results/review-report.md, results/human-review-decisions.md

## Entry 05 - Coder-agent Fixes

Stage: Fix cycle

Prompt/goal: Address only the accepted or modified findings in results/human-review-decisions.md.
Rules:
- Do not expand scope.
- Do not change requirements/specification.
- Do not weaken tests.
- Add or update regression tests when required.
- Re-run the repository verification command.
- Update results/coder-report.md with a Fix Cycle section.

When finished, stop. Do not self-approve.

AI contribution: All accepted and modified findings from the review report were cleanly resolved without introducing regressions. A new test case was added to `tests/cli.py` to resolve **RF-01** and the tracebility matrix was updated to reflect this new test case + all new 9 test cases added in `tests/test_storage.py`. A `.gitignore` file was also created and `.pyc` files were removed from git tracking.

Student decision: Another human review was done and all changes were reviewwd and accepted. When running `./script/verify_repo.sh` in Git Bash, all 4 test steps PASSED.

Impact: results/coder-report.md, tests/cli.py, docs/tracebility.md

## Entry 06 - Review Agent Re-evaluation

Stage: Re-review

Prompt/goal: Re-review the updated PR candidate.
Inputs:
- original review report,
- human review decisions,
- updated diff,
- updated verification report,
- relevant requirements, architecture, code and tests.
For each accepted/modified finding:
- RESOLVED
- PARTIALLY RESOLVED
- NOT RESOLVED

Also report any NEW MUST FIX regression introduced by the fixes.
Do not modify code.

AI contribution: The reviewer marked all accepted and modified findings from the review report as **RESOLVED** and did not find any other regressions or issues.

Student decision: Repository verification was run and all 4 test steps PASSED. All `.pyc` files seem untracked from commit and CLI test was indeed added to check for message "ERROR: Failed to load customer records: invalid record at index 0".

Impact: results/re-review-report.md, PR_EVIDENCE.md