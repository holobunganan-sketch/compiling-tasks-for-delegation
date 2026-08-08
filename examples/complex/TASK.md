# Task

## Goal
Validate an existing project's test command and produce a test-status report without changing project files.

## Deliverables
- `EXECUTION_REPORT.md` containing the observed test command and result.

## Constraints
- Read-only inspection of project files.
- Run only a test command already defined by the project.

## Delegation Summary
SAFE_TO_DELEGATE for inspection and execution when exactly one test command is present; CONDITIONAL when command presence must be checked; HIGH_MODEL_REQUIRED if multiple materially different test commands require selection.
