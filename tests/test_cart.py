import pytest
from src.product import Product
from src.cart import Cart


@pytest.fixture
def product():
    return Product("A1", "Notebook", 1250, 4)


@pytest.fixture
def cart():
    return Cart()


def test_cart_add_product_increases_items_count(cart, product):
    cart.add_product(product, 2)
    assert cart.get_items_count() == 2
    assert cart.get_subtotal() == 2500


def test_cart_add_same_instance_sums_quantity(cart, product):
    cart.add_product(product, 1)
    cart.add_product(product, 2)
    assert cart.get_items_count() == 3
    items = cart.get_items()
    assert len(items) == 1
    assert items[0]["quantity"] == 3


def test_cart_add_exceeds_stock_raises_and_cart_unchanged(cart, product):
    cart.add_product(product, 1)
    with pytest.raises(ValueError):
        cart.add_product(product, 4)
    assert cart.get_items_count() == 1


def test_cart_add_different_instance_same_id_raises(cart, product):
    cart.add_product(product, 1)
    other = Product("A1", "Other", 500, 10)
    with pytest.raises(ValueError):
        cart.add_product(other, 1)
    assert cart.get_items_count() == 1


def test_cart_add_non_product_raises(cart):
    with pytest.raises(TypeError):
        cart.add_product("not-a-product", 1)


def test_cart_remove_full_and_partial(cart, product):
    cart.add_product(product, 3)
    cart.remove_product("A1", 1)
    assert cart.get_items_count() == 2
    cart.remove_product("A1")
    assert cart.get_items_count() == 0


def test_cart_remove_unknown_raises_key_error(cart):
    with pytest.raises(KeyError):
        cart.remove_product("unknown")


def test_cart_remove_quantity_exceeds_raises(cart, product):
    cart.add_product(product, 2)
    with pytest.raises(ValueError):
        cart.remove_product("A1", 5)
    assert cart.get_items_count() == 2
