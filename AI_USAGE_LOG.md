# AI Usage Log

## Entry 01 - Initial Repository Change

Stage: Change Request

Prompt/goal: Review the branch 'after' of the repository https://github.com/VickySS2020/ada-08-agent-ready-repository.git, and propose a small but sufficient change that requires review. Don't propose changes like this:
- Format or comment changes.
- A task without verifiable criteria.
- A change so big it can't be reviewed in a single session.
- A new feature that requires redesigning the whole architecture.

AI contribution: The agent reviewed the repository documentation, source structure, and tests. It suggested changing verify_repo.sh, and also suggested adding a validation rule that verifies that customer records with an empty or whitespace-only name or email are NOT accepted.

Student decision:  
I reviewed the findings against the repository files and confirmed that `model.py` only checks that the "name" or "email" attribute is a string, it does not deal with empty or whitespace-only values. I rejected the other proposal, since it was directed at a vital document of our agent-ready repository that is outside the project's scope.

Impact:
CHANGE_REQUEST.md
