
from datagate.loader import load_data
import pandas as pd


def main():
    data = load_data()
    items = data["items"]
    payments = data["payments"]
    orders = data["orders"]

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

    comparison["difference"] = (
        comparison["item_total"] -
        comparison["payment_total"]
    )

    mismatches = comparison[
        comparison["difference"].abs() > 0.05
    ].copy()

    # Add order status for investigation.
    mismatches = mismatches.merge(
        orders[["order_id", "order_status"]],
        on="order_id",
        how="left"
    )

    print("========== MISMATCHES BY ORDER STATUS ==========")
    print(mismatches["order_status"].value_counts().to_string())

    print("\n========== PAYMENT TYPES IN MISMATCHED ORDERS ==========")
    mismatch_ids = mismatches["order_id"]
    mismatch_payments = payments[
        payments["order_id"].isin(mismatch_ids)
    ]

    print(mismatch_payments["payment_type"].value_counts().to_string())

    print("\n========== FIRST 10 MISMATCHES ==========")
    print(
        mismatches[
            ["order_id", "order_status", "item_total",
             "payment_total", "difference"]
        ].head(10).round(2).to_string(index=False)
    )


if __name__ == "__main__":
    main()