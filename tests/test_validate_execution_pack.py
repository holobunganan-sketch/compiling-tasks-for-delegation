import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_execution_pack.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validator", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("validator module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def write(self, root: Path, name: str, content: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_valid_single_file_plan_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(
                root,
                "EXECUTION_PLAN.md",
                "# Execution Plan\n\n"
                "## Task Goal\nShip the result.\n\n"
                "## Constraints\n- Preserve inputs.\n\n"
                "## Environment\n- Shell available.\n\n"
                "## Steps\n\n"
                "### STEP 01 — Inspect input\n"
                "Delegation: SAFE_TO_DELEGATE\n\n"
                "#### Purpose\nConfirm the source exists.\n\n"
                "#### Input\n`input.txt`\n\n"
                "#### Action\nRead `input.txt`.\n\n"
                "#### Expected Result\nThe file is readable.\n\n"
                "#### Evidence\nRecord the path and size.\n\n"
                "#### Verdict\nPASS or STOP.\n\n"
                "#### Exception Handling\nIf absent, stop with `E03-MISSING-INPUT`.\n\n"
                "## Acceptance Criteria\n- The source was inspected.\n\n"
                "## Final Report\nUse the required execution report format.\n",
            )
            errors = self.validator.validate_path(root)
            self.assertEqual(errors, [])

    def test_valid_multi_file_package_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(root, "TASK.md", "# Task\n\n## Goal\nShip.\n\n## Deliverables\n- Result.\n\n## Constraints\n- Preserve source.\n\n## Delegation Summary\nSAFE_TO_DELEGATE\n")
            self.write(root, "CONTEXT.md", "# Context\n\n## Known Facts\n- Input exists.\n\n## Environment\n- Shell.\n\n## Assumptions\n- None.\n\n## Boundaries\n- No destructive actions.\n")
            self.write(root, "STEPS.md", "# Steps\n\n### STEP 01 — Inspect\nDelegation: SAFE_TO_DELEGATE\n\n#### Purpose\nInspect.\n\n#### Input\n`input.txt`\n\n#### Action\nRead it.\n\n#### Expected Result\nReadable.\n\n#### Evidence\nRecord path.\n\n#### Verdict\nPASS.\n\n#### Exception Handling\nIf absent, `E03-MISSING-INPUT`.\n")
            self.write(root, "ACCEPTANCE.md", "# Acceptance\n\n## Acceptance Criteria\n- Input was inspected.\n\n## Validation Procedure\nCheck evidence.\n\n## Failure Conditions\nMissing evidence fails acceptance.\n")
            self.write(root, "EXECUTION_REPORT.md", "# Execution Report\n\n## Status\nPENDING\n\n## Completed Steps\nNone yet.\n\n## Evidence\nPending.\n\n## Deviations\nNONE\n\n## Stop Codes\nNONE\n\n## Deliverables\nPending.\n\n## Unresolved Issues\nNONE\n")
            errors = self.validator.validate_path(root)
            self.assertEqual(errors, [])

    def test_missing_required_multi_file_is_reported(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(root, "TASK.md", "# Task\n")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("missing required file" in e.lower() for e in errors))

    def test_placeholder_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(root, "EXECUTION_PLAN.md", "# Execution Plan\n\n## Task Goal\nTODO\n")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("placeholder" in e.lower() for e in errors))

    def test_invalid_delegation_state_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(
                root,
                "EXECUTION_PLAN.md",
                "# Execution Plan\n\n## Task Goal\nShip.\n\n## Constraints\n- A.\n\n## Environment\n- B.\n\n## Steps\n\n### STEP 01 — Do\nDelegation: MAYBE\n\n#### Purpose\nDo.\n\n#### Input\nA.\n\n#### Action\nAct.\n\n#### Expected Result\nDone.\n\n#### Evidence\nProof.\n\n#### Verdict\nPASS.\n\n#### Exception Handling\nStop with `E16-DECISION-REQUIRED`.\n\n## Acceptance Criteria\n- Done.\n\n## Final Report\nReport.\n",
            )
            errors = self.validator.validate_path(root)
            self.assertTrue(any("delegation" in e.lower() for e in errors))

    def test_step_missing_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write(
                root,
                "EXECUTION_PLAN.md",
                "# Execution Plan\n\n## Task Goal\nShip.\n\n## Constraints\n- A.\n\n## Environment\n- B.\n\n## Steps\n\n### STEP 01 — Do\nDelegation: SAFE_TO_DELEGATE\n\n#### Purpose\nDo.\n\n#### Input\nA.\n\n#### Action\nAct.\n\n#### Expected Result\nDone.\n\n#### Verdict\nPASS.\n\n#### Exception Handling\nStop with `E16-DECISION-REQUIRED`.\n\n## Acceptance Criteria\n- Done.\n\n## Final Report\nReport.\n",
            )
            errors = self.validator.validate_path(root)
            self.assertTrue(any("evidence" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
