"""Calculate weighted totals from human-entered AI response evaluation scores.

This script does not evaluate AI responses, infer missing scores, or call any
AI API. It only calculates weighted totals when a human evaluator has entered
valid numeric scores in data/evaluation_sheet.csv.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVALUATION_FILE = PROJECT_ROOT / "data" / "evaluation_sheet.csv"
WEIGHTS_FILE = PROJECT_ROOT / "scoring_weights.csv"
OUTPUT_FILE = PROJECT_ROOT / "reports" / "scored_results.csv"

CRITERION_TO_COLUMN = {
    "Instruction Following": "instruction_following",
    "Factual Accuracy": "factual_accuracy",
    "Completeness": "completeness",
    "Reasoning Quality": "reasoning_quality",
    "Clarity & Structure": "clarity_structure",
    "Safety & Risk Awareness": "safety_risk_awareness",
    "Korean Localization": "korean_localization",
    "Conciseness": "conciseness",
}

EVALUATION_FIELDS = [
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
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            return []
        return list(reader)


def read_weights(path: Path) -> dict[str, float]:
    rows = read_csv_rows(path)
    weights: dict[str, float] = {}

    for row_number, row in enumerate(rows, start=2):
        criterion = (row.get("criterion") or "").strip()
        raw_weight = (row.get("weight") or "").strip()

        if not criterion:
            raise ValueError(f"Missing criterion in {path} row {row_number}")
        try:
            weights[criterion] = float(raw_weight)
        except ValueError as exc:
            raise ValueError(
                f"Invalid weight for {criterion!r} in {path} row {row_number}: {raw_weight!r}"
            ) from exc

    missing = set(CRITERION_TO_COLUMN) - set(weights)
    if missing:
        raise ValueError(f"Missing weights for criteria: {', '.join(sorted(missing))}")

    return weights


def parse_score(raw_value: str, field_name: str, row_number: int) -> float | None:
    value = (raw_value or "").strip()
    if value == "":
        return None

    try:
        score = float(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid score in row {row_number}, field {field_name}: {value!r}"
        ) from exc

    if score < 0 or score > 4:
        raise ValueError(
            f"Score out of range in row {row_number}, field {field_name}: {score}"
        )

    return score


def calculate_row(row: dict[str, str], weights: dict[str, float], row_number: int) -> dict[str, str]:
    total = 0.0
    missing_fields: list[str] = []

    for criterion, field_name in CRITERION_TO_COLUMN.items():
        score = parse_score(row.get(field_name, ""), field_name, row_number)
        if score is None:
            missing_fields.append(field_name)
            continue
        total += score * weights[criterion]

    result = dict(row)
    if missing_fields:
        result["weighted_total"] = ""
        result["score_status"] = "incomplete_missing_scores"
        result["missing_score_fields"] = ";".join(missing_fields)
    else:
        result["weighted_total"] = f"{total:.2f}"
        result["score_status"] = "complete_human_scored"
        result["missing_score_fields"] = ""

    return result


def write_results(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    base_fields = list(rows[0].keys()) if rows else EVALUATION_FIELDS
    extra_fields = ["weighted_total", "score_status", "missing_score_fields"]
    fieldnames = list(dict.fromkeys(base_fields + extra_fields))

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    try:
        weights = read_weights(WEIGHTS_FILE)
        evaluation_rows = read_csv_rows(EVALUATION_FILE)
        scored_rows = [
            calculate_row(row, weights, row_number)
            for row_number, row in enumerate(evaluation_rows, start=2)
        ]
        write_results(scored_rows, OUTPUT_FILE)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    complete_count = sum(
        1 for row in scored_rows if row.get("score_status") == "complete_human_scored"
    )
    incomplete_count = len(scored_rows) - complete_count

    print("Scoring calculation finished.")
    print(f"Input evaluations: {len(scored_rows)}")
    print(f"Complete human-scored rows: {complete_count}")
    print(f"Incomplete rows with missing scores: {incomplete_count}")
    print(f"Output file: {OUTPUT_FILE}")
    print("No AI-based evaluation or score inference was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
