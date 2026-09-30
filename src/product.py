from .validation import require_int, require_text


class Product:
    def __init__(self, product_id, name, price_cents, stock):
        self.product_id = require_text(product_id, "product_id")
        self.name = require_text(name, "name")
        self.price_cents = require_int(price_cents, "price_cents", 1)
        self.stock = require_int(stock, "stock")

    def is_available(self, quantity=1):
        require_int(quantity, "quantity", 1)
        return self.stock >= quantity

    def set_stock(self, stock):
        self.stock = require_int(stock, "stock")
