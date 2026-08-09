# Acceptance

## Acceptance Criteria
- Empty names are rejected by the target utility.
- Existing non-empty-name behavior remains green.
- Both chunks have PASS evidence.

## Validation Procedure
Review the focused `pytest` output recorded by each chunk and confirm the final diff is limited to the two allowed files.

## Failure Conditions
Any failed focused test, unrelated file modification, or missing chunk evidence fails acceptance.
