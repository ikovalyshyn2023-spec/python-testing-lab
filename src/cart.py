from .product import Product
from .validation import require_int, require_text


class Cart:
    def __init__(self):
        self._items = {}  # product_id -> (Product, quantity)

    def add_product(self, product, quantity=1):
        if not isinstance(product, Product):
            raise TypeError("product must be a Product")
        require_int(quantity, "quantity", 1)
        current = self._items.get(product.product_id)
        if current is not None and current[0] is not product:
            raise ValueError("different product with the same ID")
        previous = 0 if current is None else current[1]
        if not product.is_available(previous + quantity):
            raise ValueError("insufficient stock")
        self._items[product.product_id] = (product, previous + quantity)

    def remove_product(self, product_id, quantity=None):
        product_id = require_text(product_id, "product_id")
        if product_id not in self._items:
            raise KeyError(product_id)
        product, previous = self._items[product_id]
        if quantity is None:
            del self._items[product_id]
            return
        require_int(quantity, "quantity", 1)
        if quantity > previous:
            raise ValueError("quantity exceeds cart amount")
        if quantity == previous:
            del self._items[product_id]
        else:
            self._items[product_id] = (product, previous - quantity)

    def get_items_count(self):
        return sum(quantity for _, quantity in self._items.values())

    def get_subtotal(self):
        return sum(
            product.price_cents * quantity
            for product, quantity in self._items.values()
        )

    def get_items(self):
        return [
            {
                "product_id": product.product_id,
                "name": product.name,
                "price_cents": product.price_cents,
                "quantity": quantity,
            }
            for product, quantity in self._items.values()
        ]
