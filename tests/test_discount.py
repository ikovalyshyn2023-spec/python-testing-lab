import pytest
from src.discount import customer_tier, calculate_discount, shipping_fee


@pytest.mark.parametrize(
    "points, expected",
    [
        (0, "basic"),
        (99, "basic"),
        (100, "silver"),
        (499, "silver"),
        (500, "gold"),
        (1000, "gold"),
    ],
)
def test_customer_tier_at_level_boundaries(points, expected):
    assert customer_tier(points) == expected


def test_customer_tier_rejects_bool_and_negative():
    with pytest.raises(TypeError):
        customer_tier(True)
    with pytest.raises(ValueError):
        customer_tier(-1)


def test_calculate_discount_zero_and_full_percent():
    assert calculate_discount(1000, 0) == 0
    assert calculate_discount(1000, 100) == 1000


def test_calculate_discount_rounds_down():
    # 101 * 10 // 100 = 10
    assert calculate_discount(101, 10) == 10
    assert calculate_discount(99, 10) == 9


def test_calculate_discount_rejects_percent_over_100():
    with pytest.raises(ValueError):
        calculate_discount(100, 101)


def test_calculate_discount_rejects_negative_and_bool():
    with pytest.raises(ValueError):
        calculate_discount(-1, 10)
    with pytest.raises(TypeError):
        calculate_discount(True, 10)


@pytest.mark.parametrize(
    "amount, tier, expected",
    [
        (4999, "basic", 1500),
        (5000, "basic", 700),
        (9999, "silver", 700),
        (10000, "basic", 0),
        (1000, "gold", 0),
        (5000, "gold", 0),
        (10000, "gold", 0),
    ],
)
def test_shipping_fee_by_amount_and_tier(amount, tier, expected):
    assert shipping_fee(amount, tier) == expected


def test_shipping_fee_rejects_unknown_tier_and_non_str():
    with pytest.raises(ValueError):
        shipping_fee(1000, "platinum")
    with pytest.raises(TypeError):
        shipping_fee(1000, 1)
