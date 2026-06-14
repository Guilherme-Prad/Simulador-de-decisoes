from dados import PHONES, USE_CASES


def score_phone(phone: dict, use_case: str, max_price: int, custom_weights: dict | None = None) -> float:
    if phone["price"] > max_price:
        return -1
    w = custom_weights if custom_weights else USE_CASES[use_case]["weights"]
    storage_score = min(100, phone["storage_max"] / 10.24)
    raw = (
        w["camera"]    * phone["camera"]
        + w["battery"] * phone["battery"]
        + w["gaming"]  * phone["gaming"]
        + w["cpu_score"] * phone["cpu_score"]
        + w["storage"] * storage_score
    )
    # use-case bonus (only when using preset weights)
    if not custom_weights and use_case in phone["best_for"]:
        raw *= 1.12
    # price efficiency
    price_ratio = 1 - (phone["price"] / 20000) * 0.15
    return raw * price_ratio


def rank_phones(use_case: str, max_price: int, filters: dict, custom_weights: dict | None = None) -> list:
    scored = []
    for p in PHONES:
        s = score_phone(p, use_case, max_price, custom_weights=custom_weights)
        if s < 0:
            continue
        if filters.get("min_storage") and p["storage_max"] < filters["min_storage"]:
            continue
        scored.append((s, p))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored
