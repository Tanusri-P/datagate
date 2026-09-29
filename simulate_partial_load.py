
from datagate.loader import load_data
from datagate.checks import check_volume


def main():
    data = load_data()
    orders = data["orders"]

    print("========== PARTIAL LOAD SIMULATION ==========")
    print(f"Original rows: {len(orders)}")

    # Simulate a partial load containing only 40% of rows.
    partial_orders = orders.head(int(len(orders) * 0.4))

    print(f"Loaded rows: {len(partial_orders)}")

    baseline = len(orders)

    result = check_volume(
        len(partial_orders),
        baseline
    )

    print("\n========== QUALITY CHECK ==========")
    print(result)

    if not result["passed"]:
        print("\nDATA QUALITY GATE: FAILED")
        print("Partial load detected!")
    else:
        print("\nDATA QUALITY GATE: PASSED")
        print("Volume is within the accepted range.")


if __name__ == "__main__":
    main()