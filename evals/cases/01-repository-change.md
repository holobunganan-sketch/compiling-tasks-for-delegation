# Case 01 — Existing repository change

## User request

"In the current repo, change the Windows app display name to Northwing everywhere it is required, keep the application ID unchanged, run the existing relevant tests, and do not refactor unrelated code. Compile this for a lower-capability executor."

## Pressure points

- Must inspect the repo before naming files.
- Must separate display-name changes from application-ID preservation.
- Must forbid unrelated refactoring.
- Must discover existing tests rather than invent commands.
- Multiple branding locations may require a bounded search and exact evidence.
