"""Validate CSV structure for a human-led AI response evaluation project.

This script checks file existence, required columns, score ranges, and simple
prompt/response links. It does not generate scores or evaluate response text.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "prompt_inventory": PROJECT_ROOT / "data" / "prompt_inventory.csv",
    "response_log": PROJECT_ROOT / "data" / "response_log.csv",
    "evaluation_sheet": PROJECT_ROOT / "data" / "evaluation_sheet.csv",
    "scoring_weights": PROJECT_ROOT / "scoring_weights.csv",
}

REQUIRED_COLUMNS = {
    "prompt_inventory": [
        "prompt_id",
        "category",
        "prompt_text",
        "user_intent",
        "explicit_constraints",
        "expected_behavior",
        "risk_area",
        "source_requirement",
        "notes",
    ],
    "response_log": [
        "response_id",
        "prompt_id",
        "model_name",
        "response_date",
        "response_text",
        "response_file_path",
        "notes",
    ],
    "evaluation_sheet": [
        "evaluation_id",
        "response_id",
        "prompt_id",
        "instruction_following",
        "factual_accuracy",
        "completeness",
        "reasoning_quality",
        "clarity_structure",
        "safety_risk_awareness",
        "korean_localization",
        "conciseness",
        "defect_tags",
        "severity",
        "overall_judgment",
        "evaluator_notes",
        "improvement_suggestion",
    ],
    "scoring_weights": ["criterion", "weight"],
}

SCORE_COLUMNS = [
    "instruction_following",
    "factual_accuracy",
    "completeness",
    "reasoning_quality",
    "clarity_structure",
    "safety_risk_awareness",
    "korean_localization",
    "conciseness",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames or []
        return fieldnames, list(reader)


def validate_required_files(errors: list[str]) -> None:
    for file_label, path in REQUIRED_FILES.items():
        if not path.exists():
            errors.append(f"Missing required file for {file_label}: {path}")


def validate_columns(file_label: str, fieldnames: list[str], errors: list[str]) -> None:
    required = REQUIRED_COLUMNS[file_label]
    missing = [column for column in required if column not in fieldnames]
    if missing:
        errors.append(f"{file_label} is missing columns: {', '.join(missing)}")


def validate_scores(rows: list[dict[str, str]], errors: list[str]) -> None:
    for row_number, row in enumerate(rows, start=2):
        for column in SCORE_COLUMNS:
            raw_value = (row.get(column) or "").strip()
            if raw_value == "":
                continue

            try:
                score = float(raw_value)
            except ValueError:
                errors.append(
                    f"evaluation_sheet row {row_number} has non-numeric score in {column}: {raw_value!r}"
                )
                continue

            if score < 0 or score > 4:
                errors.append(
                    f"evaluation_sheet row {row_number} has score outside 0-4 in {column}: {score}"
                )


def collect_nonblank_ids(rows: list[dict[str, str]], id_column: str) -> set[str]:
    return {
        (row.get(id_column) or "").strip()
        for row in rows
        if (row.get(id_column) or "").strip()
    }


def validate_links(
    prompt_rows: list[dict[str, str]],
    response_rows: list[dict[str, str]],
    evaluation_rows: list[dict[str, str]],
    warnings: list[str],
) -> None:
    prompt_ids = collect_nonblank_ids(prompt_rows, "prompt_id")
    response_ids = collect_nonblank_ids(response_rows, "response_id")

    for row_number, row in enumerate(response_rows, start=2):
        prompt_id = (row.get("prompt_id") or "").strip()
        if prompt_id and prompt_id not in prompt_ids:
            warnings.append(
                f"response_log row {row_number} references missing prompt_id: {prompt_id}"
            )

    for row_number, row in enumerate(evaluation_rows, start=2):
        prompt_id = (row.get("prompt_id") or "").strip()
        response_id = (row.get("response_id") or "").strip()

        if not prompt_id:
            warnings.append(f"evaluation_sheet row {row_number} has blank prompt_id")
        elif prompt_id not in prompt_ids:
            warnings.append(
                f"evaluation_sheet row {row_number} references missing prompt_id: {prompt_id}"
            )

        if not response_id:
            warnings.append(f"evaluation_sheet row {row_number} has blank response_id")
        elif response_id not in response_ids:
            warnings.append(
                f"evaluation_sheet row {row_number} references missing response_id: {response_id}"
            )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    csv_data: dict[str, tuple[list[str], list[dict[str, str]]]] = {}

    validate_required_files(errors)
    if errors:
        print("Validation failed.")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    for file_label, path in REQUIRED_FILES.items():
        fieldnames, rows = read_csv(path)
        csv_data[file_label] = (fieldnames, rows)
        validate_columns(file_label, fieldnames, errors)

    validate_scores(csv_data["evaluation_sheet"][1], errors)
    validate_links(
        csv_data["prompt_inventory"][1],
        csv_data["response_log"][1],
        csv_data["evaluation_sheet"][1],
        warnings,
    )

    if errors:
        print("Validation failed.")
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("Validation passed.")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"WARNING: {warning}")
    else:
        print("No link warnings found.")

    print("No scores were generated and no response text was evaluated.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
