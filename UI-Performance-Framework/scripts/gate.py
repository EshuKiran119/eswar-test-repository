"""Evaluate JMeter CSV evidence; engine exit 0 alone does not mean tests passed."""

import argparse
import csv
import json
import math
from pathlib import Path


def evaluate(path, label, p95_limit, error_limit):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"timeStamp", "elapsed", "label", "success"} <= rows[0].keys():
        raise ValueError("Missing or malformed JTL evidence")
    selected = [r for r in rows if r["label"] == label]
    if not selected:
        raise ValueError(f"No samples for business label {label!r}")
    durations = sorted(float(r["elapsed"]) for r in selected)
    error_rate = sum(r["success"].lower() != "true" for r in selected) / len(selected)
    # Any failed child/cleanup sample remains a failed run even when aggregation hides it.
    failed_rows = sum(r["success"].lower() != "true" for r in rows)
    p95 = durations[max(0, math.ceil(len(durations) * 0.95) - 1)]
    start = min(float(r["timeStamp"]) for r in selected)
    end = max(float(r["timeStamp"]) + float(r["elapsed"]) for r in selected)
    result = {
        "label": label,
        "samples": len(selected),
        "p95_ms": p95,
        "error_rate": error_rate,
        "failed_rows": failed_rows,
        "completed_journeys_per_second": len(selected)
        / max((end - start) / 1000, 0.001),
        "budgets": {"p95_ms": p95_limit, "error_rate": error_limit},
        "passed": p95 < p95_limit and error_rate <= error_limit and failed_rows == 0,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jtl", type=Path)
    parser.add_argument("--label", default="TXN | checkout")
    parser.add_argument("--p95-ms", type=float, default=2000)
    parser.add_argument("--error-rate", type=float, default=0.01)
    args = parser.parse_args()
    try:
        result = evaluate(args.jtl, args.label, args.p95_ms, args.error_rate)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, f"Evidence error: {error}\n")
    args.jtl.with_suffix(".gate.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
