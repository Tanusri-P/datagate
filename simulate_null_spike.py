
from datagate.loader import load_data
from datagate.checks import check_nulls


def main():
    data = load_data()
    items = data["items"].copy()

    print("========== NULL SPIKE SIMULATION ==========")
    print(f"Original rows: {len(items)}")

    # Simulate a 15% null spike in the price column.
    null_count = int(len(items) * 0.15)
    items.loc[items.index[:null_count], "price"] = float("nan")

    print(f"Artificial nulls added: {null_count}")

    result = check_nulls(
        items,
        "price",
        max_null_rate=0.05
    )

    print("\n========== QUALITY CHECK ==========")
    print(result)

    if not result["passed"]:
        print("\nDATA QUALITY GATE: FAILED")
        print("Null spike detected!")
    else:
        print("\nDATA QUALITY GATE: PASSED")
        print("Null rate is within the accepted range.")


if __name__ == "__main__":
    main()