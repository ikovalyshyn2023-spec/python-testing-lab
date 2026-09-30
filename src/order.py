from .cart import Cart
from .discount import calculate_discount, customer_tier, shipping_fee
from .validation import require_int


class Order:
    def __init__(self, cart, customer_points=0):
        if not isinstance(cart, Cart):
            raise TypeError("cart must be a Cart")
        self.customer_points = require_int(customer_points, "customer_points")
        self._cart = cart
        self.status = "draft"
        self.summary = None

    def place(self):
        if self.status != "draft":
            raise ValueError("only a draft order can be placed")
        if self._cart.get_items_count() == 0:
            raise ValueError("cannot place an empty order")
        tier = customer_tier(self.customer_points)
        percent = {"basic": 0, "silver": 5, "gold": 10}[tier]
        subtotal = self._cart.get_subtotal()
        discount = calculate_discount(subtotal, percent)
        discounted_subtotal = subtotal - discount
        delivery = shipping_fee(discounted_subtotal, tier)
        self.summary = {
            "items": self._cart.get_items(),
            "subtotal_cents": subtotal,
            "discount_cents": discount,
            "shipping_cents": delivery,
            "total_cents": discounted_subtotal + delivery,
            "tier": tier,
        }
        self.status = "placed"
        return self.summary.copy()

    def cancel(self):
        if self.status != "placed":
            raise ValueError("only a placed order can be cancelled")
        self.status = "cancelled"
