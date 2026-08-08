# Forward-test cases

These cases test whether a capable model using the skill removes reasoning burden before handing work to a weaker executor.

Run each case twice when an agent harness is available:

1. baseline without this skill;
2. with `compiling-tasks-for-delegation` loaded.

Score with `rubric.md`. The skill passes a case only when every critical criterion passes. Structural validation alone cannot prove model behavior, so these cases are retained for forward-testing across models.
