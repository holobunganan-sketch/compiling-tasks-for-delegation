# Task Delegation Compiler Implementation Plan

> **For agentic workers:** implement task-by-task with tests before validator behavior changes.

**Goal:** Ship an installable, documented Agent Skill that compiles complex user requests into deterministic execution packages for lower-capability models.

**Architecture:** Keep the root `SKILL.md` concise and delegate detail to focused references. Provide reusable templates, a structural validator, evaluation scenarios, CI, and release automation. The repository root is itself the installable skill directory.

**Tech Stack:** Markdown, Python 3 standard library, GitHub Actions.

## Global Constraints

- Support simple single-file and complex multi-file execution packages.
- Enforce three delegation states: `SAFE_TO_DELEGATE`, `CONDITIONAL`, `HIGH_MODEL_REQUIRED`.
- Preserve user intent and explicit constraints.
- Require live-context inspection when execution depends on current state.
- Keep executor discretion bounded and use stop codes for uncovered branches.
- Require evidence for verifiable steps and final execution reporting.

### Task 1: Validator tests

**Files:**
- Create: `tests/test_validate_execution_pack.py`

- [x] Write tests for valid single-file, valid multi-file, missing headers, placeholders, and invalid delegation states.
- [x] Run tests before the validator exists and confirm failure.

### Task 2: Validator implementation

**Files:**
- Create: `scripts/validate_execution_pack.py`

- [x] Implement package discovery and structural checks.
- [x] Run tests and confirm pass.

### Task 3: Skill protocol and references

**Files:**
- Create: `SKILL.md`
- Create: `references/*.md`

- [x] Encode trigger, compilation workflow, delegation policy, task taxonomy, environment adaptation, evidence, stop codes, and compiler audit.

### Task 4: Output templates and evals

**Files:**
- Create: `templates/*.md`
- Create: `evals/*`

- [x] Provide single-file and multi-file templates.
- [x] Provide representative pressure cases and scoring rubric.

### Task 5: Repository documentation and automation

**Files:**
- Create: `README.md`, `VERSION`, `CHANGELOG.md`, `LICENSE`, `RELEASE_NOTES.md`
- Create: `.github/workflows/ci.yml`, `.github/workflows/release.yml`

- [x] Document installation, usage, architecture, and package contract.
- [x] Add CI validation.
- [x] Add version-triggered tag + GitHub Release ZIP automation.

### Task 6: Verification and packaging

- [ ] Run unit tests.
- [ ] Run the validator against example packages.
- [ ] Scan for `TODO`/`TBD` in production skill files.
- [ ] Build `compiling-tasks-for-delegation-v1.0.0.zip` with the skill directory as the archive root.
- [ ] Publish repository content and verify the release workflow.
