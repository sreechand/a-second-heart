#!/usr/bin/env python3
"""Build a Literary Clock corpus after expanding multi-time quotes."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = ["time", "timestring", "quote", "title", "author"]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle, delimiter="|")
        if reader.fieldnames != FIELDS:
            raise ValueError(f"{path} must have columns: {'|'.join(FIELDS)}")
        rows = []
        for number, row in enumerate(reader, start=2):
            if any(row.get(field) is None for field in FIELDS):
                raise ValueError(f"{path}:{number} is missing a required column")
            rows.append({field: row[field].strip() for field in FIELDS})
        return rows


def quote_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["quote"], row["title"], row["author"]


def timestamp_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return row["time"], row["quote"], row["title"], row["author"]


def sort_key(row: dict[str, str]) -> tuple[int, str, str, str]:
    try:
        hour, minute = (int(piece) for piece in row["time"].split(":", 1))
    except ValueError as error:
        raise ValueError(f"Invalid time value: {row['time']}") from error
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError(f"Invalid time value: {row['time']}")
    return hour * 60 + minute, row["quote"], row["title"], row["author"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=Path, help="Current corpus CSV")
    parser.add_argument("expanded", type=Path, help="Per-timestamp replacement CSV")
    parser.add_argument("output", type=Path, help="Where to write the combined corpus")
    parser.add_argument("--expected-records", type=int)
    args = parser.parse_args()

    base_rows = read_rows(args.base)
    expanded_rows = read_rows(args.expanded)

    unique_expanded = {timestamp_key(row): row for row in expanded_rows}
    expanded_quote_keys = {quote_key(row) for row in unique_expanded.values()}
    retained = [row for row in base_rows if quote_key(row) not in expanded_quote_keys]
    result = sorted([*retained, *unique_expanded.values()], key=sort_key)

    if args.expected_records is not None and len(result) != args.expected_records:
        raise SystemExit(
            f"Expected {args.expected_records} records, built {len(result)} instead."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="|")
        writer.writeheader()
        writer.writerows(result)

    print(f"Wrote {len(result)} records to {args.output}")


if __name__ == "__main__":
    main()
