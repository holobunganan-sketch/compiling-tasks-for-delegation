#!/usr/bin/env python3
"""Validate execution packages produced by compiling-tasks-for-delegation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VALID_DELEGATION = {
    "SAFE_TO_DELEGATE",
    "CONDITIONAL",
    "HIGH_MODEL_REQUIRED",
}

PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|XXX)\b", re.IGNORECASE)
STEP_RE = re.compile(r"(?m)^###\s+STEP\s+\d+\b.*$")
DELEGATION_RE = re.compile(r"(?m)^Delegation:\s*([A-Z_]+)\s*$")

SINGLE_REQUIRED_SECTIONS = [
    "## Task Goal",
    "## Constraints",
    "## Environment",
    "## Steps",
    "## Acceptance Criteria",
    "## Final Report",
]

MULTI_REQUIRED_FILES = [
    "TASK.md",
    "CONTEXT.md",
    "STEPS.md",
    "ACCEPTANCE.md",
    "EXECUTION_REPORT.md",
]

MULTI_REQUIRED_SECTIONS = {
    "TASK.md": ["## Goal", "## Deliverables", "## Constraints", "## Delegation Summary"],
    "CONTEXT.md": ["## Known Facts", "## Environment", "## Assumptions", "## Boundaries"],
    "ACCEPTANCE.md": ["## Acceptance Criteria", "## Validation Procedure", "## Failure Conditions"],
    "EXECUTION_REPORT.md": [
        "## Status",
        "## Completed Steps",
        "## Evidence",
        "## Deviations",
        "## Stop Codes",
        "## Deliverables",
        "## Unresolved Issues",
    ],
}

STEP_REQUIRED_FIELDS = [
    "#### Purpose",
    "#### Input",
    "#### Action",
    "#### Expected Result",
    "#### Evidence",
    "#### Verdict",
    "#### Exception Handling",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


def placeholder_errors(label: str, text: str) -> list[str]:
    errors: list[str] = []
    for match in PLACEHOLDER_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: placeholder token '{match.group(0)}' is not allowed")
    return errors


def required_section_errors(label: str, text: str, sections: list[str]) -> list[str]:
    return [f"{label}: missing required section '{section}'" for section in sections if section not in text]


def split_steps(text: str) -> list[tuple[str, str]]:
    matches = list(STEP_RE.finditer(text))
    steps: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        steps.append((match.group(0).strip(), text[start:end]))
    return steps


def validate_steps(label: str, text: str) -> list[str]:
    errors: list[str] = []
    steps = split_steps(text)
    if not steps:
        return [f"{label}: no '### STEP NN' blocks found"]

    for title, block in steps:
        d = DELEGATION_RE.search(block)
        if not d:
            errors.append(f"{label}: {title}: missing Delegation state")
        elif d.group(1) not in VALID_DELEGATION:
            errors.append(
                f"{label}: {title}: invalid Delegation state '{d.group(1)}'; "
                f"expected one of {sorted(VALID_DELEGATION)}"
            )
        for field in STEP_REQUIRED_FIELDS:
            if field not in block:
                errors.append(f"{label}: {title}: missing step field '{field}'")
    return errors


def validate_single(path: Path) -> list[str]:
    text = read_text(path)
    errors = []
    errors.extend(placeholder_errors(path.name, text))
    errors.extend(required_section_errors(path.name, text, SINGLE_REQUIRED_SECTIONS))
    if "## Steps" in text:
        errors.extend(validate_steps(path.name, text))
    return errors


def validate_multi(root: Path) -> list[str]:
    errors: list[str] = []
    for name in MULTI_REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"{root}: missing required file '{name}'")

    if errors:
        return errors

    for name, sections in MULTI_REQUIRED_SECTIONS.items():
        text = read_text(root / name)
        errors.extend(placeholder_errors(name, text))
        errors.extend(required_section_errors(name, text, sections))

    steps_text = read_text(root / "STEPS.md")
    errors.extend(placeholder_errors("STEPS.md", steps_text))
    errors.extend(validate_steps("STEPS.md", steps_text))
    return errors


def validate_path(path: str | Path) -> list[str]:
    root = Path(path).resolve()
    if root.is_file():
        if root.name != "EXECUTION_PLAN.md":
            return [f"{root}: single-file validation requires EXECUTION_PLAN.md"]
        return validate_single(root)

    if not root.exists():
        return [f"{root}: path does not exist"]
    if not root.is_dir():
        return [f"{root}: path is not a directory"]

    single = root / "EXECUTION_PLAN.md"
    if single.is_file():
        return validate_single(single)

    if any((root / name).exists() for name in MULTI_REQUIRED_FILES):
        return validate_multi(root)

    return [
        f"{root}: no execution package found; expected EXECUTION_PLAN.md "
        f"or {', '.join(MULTI_REQUIRED_FILES)}"
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to EXECUTION_PLAN.md or an execution-package directory")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    errors = validate_path(args.path)
    payload = {"valid": not errors, "errors": errors}
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
    else:
        print("VALID")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
