# Compiler Audit

A package is ready only when every applicable check passes.

## Contract integrity

- The user's final goal is preserved.
- Every requested deliverable is represented.
- Explicit constraints and prohibitions are preserved.
- Prior user decisions are not reopened without evidence that they became invalid.
- No unrequested scope expansion is hidden in the steps.

## Context integrity

- Live context was inspected whenever it could change execution.
- Facts, compiler decisions, and assumptions are distinguishable.
- Paths, versions, branches, IDs, tools, and environment details are observed or intentionally conditional.

## Delegation integrity

- Every executable unit has one valid delegation state.
- `CONDITIONAL` units define the gate and both outcomes.
- `HIGH_MODEL_REQUIRED` units explain the exact unresolved judgment or authorization.
- No lower-capability executor is asked to reinterpret the user's intent.

## Step integrity

- Every step has Purpose, Input, Action, Expected Result, Evidence, Verdict, and Exception Handling.
- Mutations and read-only operations are distinguishable.
- Vague verbs are replaced by exact operations or decision rules.
- Branches are based on observable conditions.
- Every undefined material branch stops with a code.
- Dependencies appear before dependent steps.

## Evidence and acceptance

- Important claims of completion have observable evidence.
- Final acceptance criteria are measurable or explicitly gated to a capable model.
- Evidence requirements do not collect unnecessary credentials, secrets, or personal data.

## Executor simulation

Starting at STEP 01, simulate each possible defined result. At every point ask:

> Can a weaker executor select the next allowed action using only the package and the observed result?

If any answer is no, repair the package. Do not hand it off.

## Mechanical validation

When the package exists as files, run:

```bash
python scripts/validate_execution_pack.py <package-path>
```

A failing validator blocks handoff.
