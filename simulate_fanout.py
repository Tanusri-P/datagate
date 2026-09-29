
from datagate.loader import load_data
import pandas as pd


def main():
    data = load_data()
    items = data["items"]
    payments = data["payments"]

    print("========== FAN-OUT JOIN SIMULATION ==========")

    # Calculate the original item revenue.
    original_revenue = items["price"].sum()

    # Intentionally create duplicate payment records
    # to simulate a faulty join.
    duplicate_payments = pd.concat(
        [payments, payments],
        ignore_index=True
    )

    # Incorrectly join items to the duplicated payments.
    faulty_join = items.merge(
        duplicate_payments[["order_id", "payment_value"]],
        on="order_id",
        how="inner"
    )

    faulty_revenue = faulty_join["price"].sum()

    print(f"Original item rows: {len(items)}")
    print(f"Rows after faulty join: {len(faulty_join)}")
    print(f"Original item revenue: {original_revenue:.2f}")
    print(f"Faulty joined revenue: {faulty_revenue:.2f}")

    if faulty_revenue > original_revenue:
        print("\nDATA QUALITY GATE: FAILED")
        print("Fan-out detected: revenue was inflated!")
    else:
        print("\nDATA QUALITY GATE: PASSED")
        print("No revenue inflation detected.")


if __name__ == "__main__":
    main()