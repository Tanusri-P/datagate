def check_schema(df, required_columns):
    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    return {
        "check": "schema",
        "passed": len(missing) == 0,
        "missing_columns": missing
    }


def check_volume(current, baseline, lower=0.5, upper=1.5):
    if baseline <= 0:
        return {
            "check": "volume",
            "passed": False,
            "message": "Invalid baseline"
        }

    ratio = current / baseline

    return {
        "check": "volume",
        "passed": lower <= ratio <= upper,
        "current": current,
        "baseline": baseline,
        "ratio": round(ratio, 2)
    }


def check_uniqueness(df, column):
    if column not in df.columns:
        return {
            "check": "uniqueness",
            "passed": False,
            "message": f"Column not found: {column}"
        }

    duplicates = int(df[column].duplicated().sum())

    return {
        "check": "uniqueness",
        "passed": duplicates == 0,
        "column": column,
        "duplicates": duplicates
    }

def check_nulls(df, column, max_null_rate=0.05):
    if column not in df.columns:
        return {
            "check": "nulls",
            "passed": False,
            "message": f"Column not found: {column}"
        }

    null_count = int(df[column].isna().sum())
    null_rate = null_count / len(df) if len(df) else 0

    return {
        "check": "nulls",
        "passed": null_rate <= max_null_rate,
        "column": column,
        "null_count": null_count,
        "null_rate": round(null_rate, 4)
    }

def check_reconciliation(python_total, sql_total, tolerance=0.01):
    difference = abs(python_total - sql_total)

    passed = difference <= tolerance

    return {
        "check": "reconciliation",
        "passed": passed,
        "python_total": round(python_total, 2),
        "sql_total": round(sql_total, 2),
        "difference": round(difference, 2)
    }