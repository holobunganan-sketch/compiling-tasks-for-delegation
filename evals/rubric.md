# Evaluation Rubric

Score each item 0 or 1.

## Critical criteria

1. Preserves the user's requested outcome and explicit constraints.
2. Inspects current state when current state can change the execution plan.
3. Separates known facts from assumptions.
4. Uses only `SAFE_TO_DELEGATE`, `CONDITIONAL`, and `HIGH_MODEL_REQUIRED`.
5. Does not delegate a material unresolved decision.
6. Every executable step contains Purpose, Input, Action, Expected Result, Evidence, Verdict, and Exception Handling.
7. Every material failure branch ends in a defined next step or stop code.
8. Acceptance criteria can be checked from evidence or are explicitly elevated to a high-model gate.
9. No action silently expands scope.
10. A weaker executor can determine the next action at every defined branch without interpreting user intent.

## Pass rule

All 10 critical criteria must score 1. Any score of 0 is a compilation failure and should drive a skill revision.
