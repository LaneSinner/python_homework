import pytest

from src.models import Product, Category

@pytest.fixture(autouse=True)
def reset_category_counts():
    Category.category_count = 0
    Category.product_count = 0

@pytest.fixture
def product1():
    return Product(
    "Samsung Galaxy S23 Ultra",
    "256GB, Серый цвет, 200MP камера",
    180000.0,
    5,
)

@pytest.fixture
def product2():
    return Product(
    "Iphone 15",
    "512GB, Gray space",
    210000.0,
    8,
)

@pytest.fixture
def product3():
    return Product(
    "Xiaomi Redmi Note 11",
    "1024GB, Синий",
    31000.0,
    14,
)

@pytest.fixture
def category1(product1, product2, product3):
    return Category(
    "Смартфоны",
    "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    [product1, product2, product3],
)

@pytest.fixture
def category2(product1):
    return Category("name","description",[product1])

@pytest.fixture
def dict():
    return {
    "name": "name",
    "description": "description",
    "price": 1.0,
    "quantity": 1

}

@pytest.fixture
def new_price():
    return 1.0

def test_product_init(product1):
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5

def test_category_init(category1):
    assert category1.name == "Смартфоны"
    assert category1.description == (
    "Смартфоны, как средство не только коммуникации, "
    "но и получения дополнительных функций для удобства жизни"
)
    assert len(category1.products.splitlines()) == 3

def test_category_count(category1):
    assert Category.category_count == 1

@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.product_count = 0
    Category.category_count = 0

def test_product_count(category1:Category,product1):
    Category.add_product(category1,product1)
    assert Category.product_count == 4

def test_products(category2:Category):
    product_str = category2.products
    assert (
    product_str == 'Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n'
)

def test_new_product(dict):
    new_product = Product.new_product(dict)
    assert new_product.name == "name"
    assert new_product.description == "description"
    assert new_product.price == 1.0
    assert new_product.quantity == 1


def test_price_getter_and_setter(product1):
    assert product1.price == 180000.0

    product1.price = 190000.0

    assert product1.price == 190000.0


@pytest.mark.parametrize("new_price", [0, -10])
def test_invalid_price_is_not_set(product1, new_price, capsys):
    old_price = product1.price

    product1.price = new_price

    assert product1.price == old_price
    assert capsys.readouterr().out.strip() == (
        "Цена не должна быть нулевая или отрицательная"
    )


    def test_product_str(product1):
         assert str(product1) == (
         "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
     )


    def test_category_str(category1):
        assert str(category1) == "Смартфоны, количество продуктов: 27 шт."


    def test_product_add(product1, product2):
         assert product1 + product2 == 180000.0 * 5 + 210000.0 * 8