
import pandas as pd

from datagate.loader import load_data
from datagate.checks import check_uniqueness


def main():
    data = load_data()
    orders = data["orders"]

    print("========== DUPLICATE BATCH SIMULATION ==========")
    print(f"Original rows: {len(orders)}")

    # Simulate a duplicate batch by appending
    # the first 1,000 orders again.
    duplicated_orders = pd.concat(
        [orders, orders.head(1000)],
        ignore_index=True
    )

    print(f"Rows after simulation: {len(duplicated_orders)}")

    # Check for duplicate order IDs.
    result = check_uniqueness(
        duplicated_orders,
        "order_id"
    )

    print("\n========== QUALITY CHECK ==========")
    print(result)

    if not result["passed"]:
        print("\nDATA QUALITY GATE: FAILED")
        print("Duplicate batch detected!")
    else:
        print("\nDATA QUALITY GATE: PASSED")
        print("No duplicate IDs detected.")


if __name__ == "__main__":
    main()