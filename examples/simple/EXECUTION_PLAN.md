# Execution Plan

## Task Goal
Verify a CSV file exists and record its header without modifying the file.

## Constraints
- Keep the source file unchanged.
- Do not infer missing columns.

## Environment
- Local filesystem access is available.
- Target path is `data/input.csv`.

## Steps

### STEP 01 — Read the CSV header
Delegation: SAFE_TO_DELEGATE

#### Purpose
Confirm the input file is readable and capture its exact column names.

#### Input
`data/input.csv`

#### Action
1. Confirm `data/input.csv` exists.
2. Read only the first line as text.
3. Do not modify the file.

#### Expected Result
The file exists and one header line is readable.

#### Evidence
Record the exact path and the first line.

#### Verdict
- PASS: the file exists and the first line is readable.
- STOP: the file is absent or unreadable.

#### Exception Handling
- File absent: `E03-MISSING-INPUT`.
- File unreadable: `E04-PERMISSION-DENIED`.

## Acceptance Criteria
- `data/input.csv` was not modified.
- The exact first line was recorded as evidence.

## Final Report
Report final status, STEP 01 verdict, evidence, deviations, stop codes, and unresolved issues.
