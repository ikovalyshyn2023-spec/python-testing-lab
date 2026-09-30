from .validation import require_int


def customer_tier(points):
    require_int(points, "points")
    if points >= 500:
        return "gold"
    if points >= 100:
        return "silver"
    return "basic"


def calculate_discount(subtotal_cents, percent):
    require_int(subtotal_cents, "subtotal_cents")
    require_int(percent, "percent")
    if percent > 100:
        raise ValueError("percent cannot exceed 100")
    return subtotal_cents * percent // 100


def shipping_fee(discounted_subtotal_cents, tier):
    require_int(discounted_subtotal_cents, "discounted_subtotal_cents")
    if not isinstance(tier, str):
        raise TypeError("tier must be a string")
    if tier not in ("basic", "silver", "gold"):
        raise ValueError("unknown tier")
    if tier == "gold" or discounted_subtotal_cents >= 10000:
        return 0
    if discounted_subtotal_cents >= 5000:
        return 700
    return 1500
