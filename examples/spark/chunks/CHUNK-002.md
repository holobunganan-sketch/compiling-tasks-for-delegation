# CHUNK-002 — Implement local validation

## Target Executor
GPT-5.3-Codex-Spark

## Chunk Goal
Implement the smallest production change that makes the empty-name test pass while preserving focused behavior.

## Why This Chunk Exists
Implementation is isolated from test-intent definition and can be verified independently.

## Required Context
- PASS evidence from CHUNK-001.
- `src/greeting.py`
- `tests/test_greeting.py`

## Context Budget
- Compiler target: <= 12,000 input tokens including required context.

## Preconditions
- CHUNK-001 status is PASS.
- The expected failing test from CHUNK-001 is still present.

## Allowed Scope
- Modify `src/greeting.py` only.
- Read `tests/test_greeting.py` for verification.

## Forbidden Actions
- Do not redesign the public API.
- Do not alter test expectations in this chunk.

## Files / Resources
- `src/greeting.py`
- `tests/test_greeting.py`

## Exact Steps

### STEP 01 — Add minimal empty-name guard
Delegation: SAFE_TO_DELEGATE

#### Purpose
Implement the behavior required by the regression test.

#### Input
`src/greeting.py`

#### Action
Add the smallest guard at the target function entry that raises `ValueError` when the name argument is empty. Preserve all other code paths.

#### Expected Result
Only the target function contains the local validation change.

#### Evidence
Record the focused production diff.

#### Verdict
PASS when the diff is limited to the empty-name guard.

#### Exception Handling
If the target function signature or behavior differs from the compiled context, stop with `E02-ENVIRONMENT-MISMATCH`.

### STEP 02 — Run focused tests
Delegation: SAFE_TO_DELEGATE

#### Purpose
Verify the requested behavior and guard against local regression.

#### Input
Updated `src/greeting.py` and existing `tests/test_greeting.py`.

#### Action
Run `python -m pytest tests/test_greeting.py -q`.

#### Expected Result
Exit status is 0 and all focused tests pass.

#### Evidence
Record the command, exit status, and pytest summary.

#### Verdict
PASS when all focused tests pass.

#### Exception Handling
If any focused test fails, stop with `E25-ACCEPTANCE-FAILED` and record the output.

### STEP 03 — Check scope
Delegation: SAFE_TO_DELEGATE

#### Purpose
Confirm no unrelated files changed.

#### Input
Current working-tree diff.

#### Action
Inspect the diff and confirm this chunk changed only `src/greeting.py`; CHUNK-001 changed only `tests/test_greeting.py`.

#### Expected Result
No unrelated changes are present.

#### Evidence
Record the changed-file list.

#### Verdict
PASS when the changed-file list matches the compiled scope.

#### Exception Handling
If unrelated changes are present, stop with `E10-SCOPE-DRIFT` without discarding user work.

## Mandatory Verification
Run `python -m pytest tests/test_greeting.py -q` and inspect the final changed-file list. Both checks must pass.

## Expected Result
The empty-name behavior is implemented, focused tests pass, and scope remains bounded.

## Evidence to Record
- Production diff.
- Passing pytest summary.
- Final changed-file list.

## Failure Branches
Failed focused verification returns `E25-ACCEPTANCE-FAILED`; scope drift returns `E10-SCOPE-DRIFT`.

## Completion Report
Report `CHUNK-002 COMPLETED`, Result, Changes, Verification, Evidence, and final acceptance status.

## Next-Chunk Gate
USER_APPROVAL_REQUIRED
AUTO_CONTINUE_FORBIDDEN

This is the final chunk. On PASS, stop after the final completion and acceptance report. No next-chunk question is required.
