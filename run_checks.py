import sqlite3
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

from config import (
    VOLUME_BASELINES,
    VOLUME_LOWER_LIMIT,
    VOLUME_UPPER_LIMIT,
)

from datagate.loader import load_data
from datagate.checks import (
    check_schema,
    check_volume,
    check_uniqueness,
    check_nulls,
    check_reconciliation,
)


def main():
    data = load_data()
    results = []

    # 1. Schema validation
    results.append(
        check_schema(
            data["orders"],
            ["order_id", "customer_id", "order_status"]
        )
    )

    results.append(
        check_schema(
            data["items"],
            ["order_id", "order_item_id", "price"]
        )
    )

    # 2. Volume validation
    orders_count = len(data["orders"])
    baseline_orders = VOLUME_BASELINES["orders"]

    results.append(
        check_volume(
            orders_count,
            baseline_orders,
            lower=VOLUME_LOWER_LIMIT,
            upper=VOLUME_UPPER_LIMIT
        )
    )

    # 3. Uniqueness validation
    results.append(
        check_uniqueness(
            data["orders"],
            "order_id"
        )
    )

    # 4. Null validation
    results.append(
        check_nulls(
            data["orders"],
            "order_id"
        )
    )

    # 5. Revenue reconciliation
    
    # 5. Revenue reconciliation
    items = data["items"]
    payments = data["payments"]

    # Calculate order totals independently.
    item_totals = (
        items.assign(
            item_total=items["price"] + items["freight_value"]
        )
        .groupby("order_id")["item_total"]
        .sum()
    )

    payment_totals = (
        payments.groupby("order_id")["payment_value"]
        .sum()
    )

    comparison = pd.concat(
        [item_totals, payment_totals],
        axis=1,
        keys=["item_total", "payment_total"]
    ).dropna()

    mismatches = (
        comparison["item_total"] -
        comparison["payment_total"]
    ).abs() > 0.05

    mismatch_count = int(mismatches.sum())

    results.append({
        "check": "reconciliation",
        "passed": mismatch_count == 0,
        "orders_compared": len(comparison),
        "mismatched_orders": mismatch_count,
        "tolerance": 0.05
    })


    # 6. Save quality artifacts
    root = Path(__file__).resolve().parent
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    passed = sum(result["passed"] for result in results)
    failed = len(results) - passed

    report = {
        "project": "DataGate",
        "generated_at": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "total_checks": len(results),
        "passed": passed,
        "failed": failed,
        "overall_status": "PASSED" if failed == 0 else "FAILED",
        "results": results
    }

    with open(
        artifacts_dir / "quality_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    pd.DataFrame(results).to_csv(
        artifacts_dir / "quality_report.csv",
        index=False
    )

    defects = [
        {
            "check": result["check"],
            "status": "OPEN",
            "details": json.dumps(result)
        }
        for result in results
        if not result["passed"]
    ]

    pd.DataFrame(
        defects,
        columns=["check", "status", "details"]
    ).to_csv(
        artifacts_dir / "defect_log.csv",
        index=False
    )

    scorecard = f"""# DataGate Quality Scorecard

Generated: {report["generated_at"]}

| Metric | Result |
|---|---:|
| Total checks | {len(results)} |
| Passed | {passed} |
| Failed | {failed} |
| Pass rate | {passed / len(results) * 100:.1f}% |
| Overall status | {report["overall_status"]} |

## Check results

| Check | Status |
|---|---|
""" + "".join(
        f"| {result['check']} | "
        f"{'PASS' if result['passed'] else 'FAIL'} |\\n"
        for result in results
    )

    (artifacts_dir / "scorecard.md").write_text(
        scorecard,
        encoding="utf-8"
    )

    
    # Print quality report
    print("\n========== DATAGATE QUALITY REPORT ==========\n")

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{result['check'].upper():20} {status}")
        print(result)

    # Summary
    passed = sum(result["passed"] for result in results)
    failed = len(results) - passed

    print("\n========== SUMMARY ==========")
    print(f"Total checks : {len(results)}")
    print(f"Passed       : {passed}")
    print(f"Failed       : {failed}")

    if failed:
        print("\nDATA QUALITY GATE: FAILED")
    else:
        print("\nDATA QUALITY GATE: PASSED")


if __name__ == "__main__":
    main()