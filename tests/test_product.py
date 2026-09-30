import pytest
from src.product import Product


@pytest.fixture
def product():
    return Product("A1", "Notebook", 1250, 4)


def test_product_constructor_sets_fields(product):
    assert product.product_id == "A1"
    assert product.name == "Notebook"
    assert product.price_cents == 1250
    assert product.stock == 4


def test_product_rejects_zero_price():
    with pytest.raises(ValueError):
        Product("A1", "X", 0, 1)


def test_product_rejects_empty_id_and_bool_stock():
    with pytest.raises(ValueError):
        Product("  ", "X", 100, 1)
    with pytest.raises(TypeError):
        Product("A1", "X", 100, True)


def test_product_is_available_at_stock_limit(product):
    assert product.is_available(4) is True
    assert product.is_available(5) is False


def test_product_is_available_rejects_zero_quantity(product):
    with pytest.raises(ValueError):
        product.is_available(0)


def test_product_set_stock_updates_value(product):
    product.set_stock(10)
    assert product.stock == 10
    assert product.is_available(10) is True


def test_product_set_stock_rejects_negative(product):
    with pytest.raises(ValueError):
        product.set_stock(-1)
