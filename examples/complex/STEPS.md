# Steps

### STEP 01 — Inspect the test script
Delegation: CONDITIONAL

#### Purpose
Determine whether the project declares one exact test command.

#### Input
`package.json`

#### Action
1. Open `package.json`.
2. Read `scripts.test`.
3. Do not modify the file.

#### Expected Result
Exactly one string value is present at `scripts.test`.

#### Evidence
Record the exact `scripts.test` value.

#### Verdict
- PASS: one string value exists -> STEP 02.
- STOP: the key is absent or the value is not one executable string.

#### Exception Handling
- Missing key: `E06-DEPENDENCY-MISSING`.
- Ambiguous/non-string value: `E16-DECISION-REQUIRED`.

### STEP 02 — Run the declared test command
Delegation: SAFE_TO_DELEGATE

#### Purpose
Observe whether the project's declared test command passes in the current environment.

#### Input
The exact command recorded from STEP 01.

#### Action
1. Run the declared test script through the project's existing package manager.
2. Do not install packages or modify configuration.

#### Expected Result
The command exits with code 0 or returns a defined failing test result.

#### Evidence
Record the exact command, exit code, and concise test summary.

#### Verdict
- PASS: exit code 0 -> final acceptance.
- STOP: nonzero exit code -> report `E09-VALIDATION-FAILED` with output summary.

#### Exception Handling
- Missing package manager or executable: `E05-TOOL-UNAVAILABLE`.
- Nonzero test exit: `E09-VALIDATION-FAILED`.
- Output cannot be classified: `E08-UNEXPECTED-OUTPUT`.
