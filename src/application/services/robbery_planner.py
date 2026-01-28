def plan_robbery(banks: list[dict], target: int) -> list[dict]:
    banks = sorted(
        banks,
        key=lambda b: (b["clients"], -b["total"])
    )

    selected = []
    total = 0

    for bank in banks:
        selected.append(bank)
        total += bank["total"]

        if total >= target:
            return selected

    return []

