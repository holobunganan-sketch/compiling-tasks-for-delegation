# CHUNK-001 — Add the focused regression test

## Target Executor
GPT-5.3-Codex-Spark

## Chunk Goal
Add one focused test that proves empty names must be rejected, after confirming the existing focused test file is green.

## Why This Chunk Exists
This creates an independently verified baseline and isolates test intent before implementation.

## Required Context
- `src/greeting.py`
- `tests/test_greeting.py`

## Context Budget
- Compiler target: <= 12,000 input tokens including required context.

## Preconditions
- Repository root is the working directory.
- Python and pytest are available.

## Allowed Scope
- Read `src/greeting.py`.
- Modify `tests/test_greeting.py` only.

## Forbidden Actions
- Do not modify production code in this chunk.
- Do not read or execute CHUNK-002.

## Files / Resources
- `src/greeting.py`
- `tests/test_greeting.py`

## Exact Steps

### STEP 01 — Confirm baseline
Delegation: SAFE_TO_DELEGATE

#### Purpose
Establish that the focused tests are green before mutation.

#### Input
`tests/test_greeting.py`

#### Action
Run `python -m pytest tests/test_greeting.py -q`.

#### Expected Result
Exit status is 0.

#### Evidence
Record the command, exit status, and pytest summary.

#### Verdict
PASS when exit status is 0.

#### Exception Handling
If the baseline fails, stop with `E11-UNEXPECTED-OUTPUT` and record the failing output.

### STEP 02 — Add empty-name regression test
Delegation: SAFE_TO_DELEGATE

#### Purpose
Encode the required behavior before implementation.

#### Input
`tests/test_greeting.py`

#### Action
Add one test asserting that an empty name raises `ValueError`. Do not modify existing assertions.

#### Expected Result
The new test is present and existing tests remain unchanged.

#### Evidence
Record the focused diff for `tests/test_greeting.py`.

#### Verdict
PASS when the diff contains only the new focused test.

#### Exception Handling
If the existing test structure makes the assertion ambiguous, stop with `E16-DECISION-REQUIRED`.

### STEP 03 — Prove the test fails for the intended reason
Delegation: SAFE_TO_DELEGATE

#### Purpose
Confirm the regression test detects the missing behavior.

#### Input
Updated `tests/test_greeting.py`.

#### Action
Run `python -m pytest tests/test_greeting.py -q`.

#### Expected Result
The new empty-name test fails because `ValueError` is not raised; unrelated focused tests pass.

#### Evidence
Record the failing test name and pytest summary.

#### Verdict
PASS when only the intended new behavior is missing.

#### Exception Handling
If failure is caused by syntax, import, fixture, or unrelated behavior, stop with `E11-UNEXPECTED-OUTPUT`.

## Mandatory Verification
Run `python -m pytest tests/test_greeting.py -q` and confirm the new test fails specifically because `ValueError` is not raised while existing focused tests remain green.

## Expected Result
A focused failing regression test exists with a clean baseline record.

## Evidence to Record
- Baseline pytest summary.
- Test-file diff.
- Expected failing-test summary.

## Failure Branches
Any unrelated baseline or regression-test failure stops with `E11-UNEXPECTED-OUTPUT`.

## Completion Report
Report `CHUNK-001 COMPLETED`, Result, Changes, Verification, Evidence, and the next planned chunk.

## Next-Chunk Gate
USER_APPROVAL_REQUIRED
AUTO_CONTINUE_FORBIDDEN

On PASS, stop and ask whether to start `CHUNK-002 — Implement local validation`. Do not read or execute CHUNK-002 before explicit user approval.
