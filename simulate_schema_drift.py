
from datagate.loader import load_data
from datagate.checks import check_schema


def main():
    data = load_data()
    items = data["items"].copy()

    print("========== SCHEMA DRIFT SIMULATION ==========")
    print(f"Original columns: {list(items.columns)}")

    # Simulate schema drift by renaming the price column.
    items.rename(
        columns={"price": "item_price"},
        inplace=True
    )

    print(f"\nModified columns: {list(items.columns)}")

    # Check whether the required column still exists.
    result = check_schema(
        items,
        ["order_id", "order_item_id", "price"]
    )

    print("\n========== QUALITY CHECK ==========")
    print(result)

    if not result["passed"]:
        print("\nDATA QUALITY GATE: FAILED")
        print("Schema drift detected!")
    else:
        print("\nDATA QUALITY GATE: PASSED")
        print("Schema is valid.")


if __name__ == "__main__":
    main()