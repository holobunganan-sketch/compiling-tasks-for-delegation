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


class SparkValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def write(self, root: Path, name: str, content: str) -> None:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def make_valid_spark_pack(self, root: Path, step_count: int = 1) -> None:
        self.write(
            root,
            "TASK.md",
            "# Task\n\n## Goal\nShip one bounded change.\n\n## Deliverables\n- Verified change.\n\n"
            "## Constraints\n- Preserve scope.\n\n## Delegation Summary\nSAFE_TO_DELEGATE\n\n"
            "## Target Executor\nGPT-5.3-Codex-Spark\n",
        )
        self.write(
            root,
            "CONTEXT.md",
            "# Context\n\n## Known Facts\n- Repository exists.\n\n## Environment\n- Codex.\n\n"
            "## Assumptions\n- None.\n\n## Boundaries\n- Stay inside the current chunk.\n",
        )
        self.write(
            root,
            "SPARK_MASTER_INDEX.md",
            "# Spark Master Index\n\n## Target Executor\nGPT-5.3-Codex-Spark\n\n"
            "## Execution Rule\nLoad only the active chunk.\n\n## Chunk Status\n- CHUNK-001: READY\n",
        )
        self.write(
            root,
            "ACCEPTANCE.md",
            "# Acceptance\n\n## Acceptance Criteria\n- Verification passes.\n\n"
            "## Validation Procedure\nReview chunk evidence.\n\n## Failure Conditions\nMissing evidence fails.\n",
        )
        self.write(
            root,
            "EXECUTION_REPORT.md",
            "# Execution Report\n\n## Status\nPENDING\n\n## Completed Steps\nNone yet.\n\n"
            "## Evidence\nPending.\n\n## Deviations\nNONE\n\n## Stop Codes\nNONE\n\n"
            "## Deliverables\nPending.\n\n## Unresolved Issues\nNONE\n",
        )
        steps = []
        for i in range(1, step_count + 1):
            steps.append(
                f"### STEP {i:02d} — Action {i}\n"
                "Delegation: SAFE_TO_DELEGATE\n\n"
                "#### Purpose\nMake one bounded change.\n\n"
                "#### Input\nCurrent repository state.\n\n"
                "#### Action\nPerform the specified edit.\n\n"
                "#### Expected Result\nThe edit is present.\n\n"
                "#### Evidence\nRecord the diff.\n\n"
                "#### Verdict\nPASS or BLOCKED.\n\n"
                "#### Exception Handling\nStop with `E11-UNEXPECTED-OUTPUT`.\n"
            )
        self.write(
            root,
            "chunks/CHUNK-001.md",
            "# CHUNK-001 — Bounded edit\n\n"
            "## Target Executor\nGPT-5.3-Codex-Spark\n\n"
            "## Chunk Goal\nComplete one bounded edit.\n\n"
            "## Why This Chunk Exists\nKeep the execution loop small.\n\n"
            "## Required Context\n- Read only the named files.\n\n"
            "## Context Budget\n- Compiler target: <= 12,000 input tokens including required context.\n\n"
            "## Preconditions\n- Repository is available.\n\n"
            "## Allowed Scope\n- One bounded edit.\n\n"
            "## Forbidden Actions\n- Do not load or execute later chunks.\n\n"
            "## Files / Resources\n- `src/example.py`\n\n"
            "## Exact Steps\n\n" + "\n".join(steps) + "\n\n"
            "## Mandatory Verification\nRun `python -m compileall src/example.py` and record the exit status.\n\n"
            "## Expected Result\nThe requested change exists and verification passes.\n\n"
            "## Evidence to Record\n- Diff\n- Verification output\n\n"
            "## Failure Branches\nIf verification fails, stop and report evidence.\n\n"
            "## Completion Report\nReport chunk status, changes, verification, and evidence.\n\n"
            "## Next-Chunk Gate\nUSER_APPROVAL_REQUIRED\nAUTO_CONTINUE_FORBIDDEN\nOn PASS, stop. Ask whether to start the next chunk. Do not preload or execute it without explicit user approval.\n",
        )

    def test_valid_spark_package_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root)
            self.assertEqual(self.validator.validate_path(root), [])

    def test_spark_chunk_over_six_steps_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root, step_count=7)
            errors = self.validator.validate_path(root)
            self.assertTrue(any("six" in e.lower() or "6" in e for e in errors))

    def test_spark_chunk_requires_mandatory_verification(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root)
            path = root / "chunks/CHUNK-001.md"
            path.write_text(path.read_text(encoding="utf-8").replace("## Mandatory Verification", "## Verification"), encoding="utf-8")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("mandatory verification" in e.lower() for e in errors))

    def test_spark_chunk_requires_next_chunk_gate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root)
            path = root / "chunks/CHUNK-001.md"
            path.write_text(path.read_text(encoding="utf-8").replace("## Next-Chunk Gate", "## Continue"), encoding="utf-8")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("next-chunk gate" in e.lower() for e in errors))

    def test_spark_package_requires_exact_target_executor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root)
            path = root / "TASK.md"
            path.write_text(path.read_text(encoding="utf-8").replace("GPT-5.3-Codex-Spark", "Other model"), encoding="utf-8")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("target executor" in e.lower() for e in errors))

    def test_spark_chunk_over_three_primary_files_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_valid_spark_pack(root)
            path = root / "chunks/CHUNK-001.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace("- `src/example.py`", "- `src/a.py`\n- `src/b.py`\n- `src/c.py`\n- `src/d.py`")
            path.write_text(text, encoding="utf-8")
            errors = self.validator.validate_path(root)
            self.assertTrue(any("primary files" in e.lower() or "files/resources" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
