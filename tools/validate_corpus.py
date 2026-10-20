#!/usr/bin/env python3
"""Validate the Literary Clock corpus before rendering images."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


FIELDS = ["time", "timestring", "quote", "title", "author"]
TIME = re.compile(r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "corpus",
        nargs="?",
        type=Path,
        default=root / "quote to image" / "litclock_annotated_br2.csv",
    )
    parser.add_argument("--expected-records", type=int)
    parser.add_argument(
        "--require-credits",
        action="store_true",
        help="Fail when a title or author is blank.",
    )
    args = parser.parse_args()

    with args.corpus.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter="|")
        if reader.fieldnames != FIELDS:
            raise SystemExit(f"Expected columns: {'|'.join(FIELDS)}")
        rows = list(reader)

    errors = []
    for number, row in enumerate(rows, start=2):
        if not TIME.fullmatch(row["time"]):
            errors.append(f"row {number}: invalid time {row['time']!r}")
        if any(not row[field].strip() for field in FIELDS[:3]):
            errors.append(f"row {number}: empty time, timestamp text, or quote")
        if args.require_credits and any(not row[field].strip() for field in FIELDS[3:]):
            errors.append(f"row {number}: empty title or author")

    if args.expected_records is not None and len(rows) != args.expected_records:
        errors.append(f"expected {args.expected_records} records, found {len(rows)}")

    if errors:
        raise SystemExit("\n".join(errors[:20]))
    print(f"Valid corpus: {len(rows)} records")


if __name__ == "__main__":
    main()
