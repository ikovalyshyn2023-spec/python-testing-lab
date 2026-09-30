import pytest
from src.product import Product
from src.cart import Cart
from src.order import Order


@pytest.fixture
def filled_cart():
    cart = Cart()
    p = Product("A1", "Notebook", 2000, 10)
    cart.add_product(p, 3)  # subtotal 6000
    return cart


def test_order_initial_status_is_draft(filled_cart):
    order = Order(filled_cart, customer_points=50)
    assert order.status == "draft"
    assert order.summary is None


def test_order_place_empty_cart_raises():
    order = Order(Cart())
    with pytest.raises(ValueError):
        order.place()
    assert order.status == "draft"


def test_order_place_basic_tier_summary(filled_cart):
    # subtotal 6000, basic 0%, shipping 700 (5000-9999)
    order = Order(filled_cart, customer_points=50)
    summary = order.place()
    assert order.status == "placed"
    assert summary["subtotal_cents"] == 6000
    assert summary["discount_cents"] == 0
    assert summary["shipping_cents"] == 700
    assert summary["total_cents"] == 6700
    assert summary["tier"] == "basic"


def test_order_place_silver_tier_summary(filled_cart):
    # 6000, 5% => discount 300, discounted 5700, shipping 700
    order = Order(filled_cart, customer_points=100)
    summary = order.place()
    assert summary["discount_cents"] == 300
    assert summary["shipping_cents"] == 700
    assert summary["total_cents"] == 6400
    assert summary["tier"] == "silver"


def test_order_place_gold_free_shipping(filled_cart):
    # 6000, 10% => 600, discounted 5400, gold => shipping 0
    order = Order(filled_cart, customer_points=500)
    summary = order.place()
    assert summary["discount_cents"] == 600
    assert summary["shipping_cents"] == 0
    assert summary["total_cents"] == 5400
    assert summary["tier"] == "gold"


def test_order_cannot_place_twice(filled_cart):
    order = Order(filled_cart, 0)
    order.place()
    with pytest.raises(ValueError):
        order.place()
    assert order.status == "placed"


def test_order_cancel_after_place(filled_cart):
    order = Order(filled_cart, 0)
    order.place()
    order.cancel()
    assert order.status == "cancelled"


def test_order_cancel_from_draft_raises(filled_cart):
    order = Order(filled_cart, 0)
    with pytest.raises(ValueError):
        order.cancel()
    assert order.status == "draft"


def test_order_summary_not_changed_when_cart_mutated(filled_cart):
    order = Order(filled_cart, 0)
    summary = order.place()
    # mutate cart after place
    p2 = Product("B2", "Pen", 100, 5)
    filled_cart.add_product(p2, 1)
    assert order.summary["subtotal_cents"] == summary["subtotal_cents"]
    assert order.summary["total_cents"] == summary["total_cents"]


def test_order_rejects_non_cart():
    with pytest.raises(TypeError):
        Order("not-a-cart")
