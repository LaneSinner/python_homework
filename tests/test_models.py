import pytest

from src.models import Category, Product, Smartphone, LawnGrass


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
    return Category("name", "description", [product1])


@pytest.fixture
def dict():
    return {"name": "name", "description": "description", "price": 1.0, "quantity": 1}


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


def test_product_count(category1: Category, product1):
    Category.add_product(category1, product1)
    assert Category.product_count == 4


def test_products(category2: Category):
    product_str = category2.products
    assert product_str == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"


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

    def test_category_accept_product(category1):
        product = Product("Тестовый товар", "Описание товара", 100, 2)
        category1.add_product(product)
        assert category1.products == [product]

    def test_category_accepts_product_subclass(category1):
        class SpecialProduct(Product):
            pass

        product = SpecialProduct("Особый товар", "Описание", 200, 1)

        category1.add_product(product)

        assert category1.products == [product]


@pytest.mark.parametrize("value", [None, "строка", 123, object()])
def test_category_rejects_non_product(category1, value):
    with pytest.raises(TypeError):
        category1.add_product(value)

def test_mixin_product(capsys):
    product = Product("Продукт1", "Описание продукта", 1200, 10)

    captured = capsys.readouterr()
    expected = "Product('Продукт1', 'Описание продукта', 1200, 10)"

    assert captured.out.strip() == expected
    assert repr(product) == expected


def test_mixin_new_product(capsys):
    product_data = {
        "name": "Продукт1",
        "description": "Описание продукта",
        "price": 1200,
        "quantity": 10,
    }
    product = Product.new_product(product_data)

    captured = capsys.readouterr()
    expected = "Product('Продукт1', 'Описание продукта', 1200, 10)"

    assert captured.out.strip() == expected
    assert repr(product) == expected


def test_mixin_smartphone(capsys):
    smartphone = Smartphone(
        "Samsung", "Смартфон", 100000, 5,
        "Высокая", "S23", 256, "черный",
    )

    captured = capsys.readouterr()
    expected = "Smartphone('Samsung', 'Смартфон', 100000, 5)"

    assert captured.out.strip() == expected
    assert repr(smartphone) == expected


def test_mixin_lawn_grass(capsys):
    grass = LawnGrass(
        "Газон", "Зеленый газон", 500, 20,
        "Россия", "7 дней", "зеленый",
    )

    captured = capsys.readouterr()
    expected = "LawnGrass('Газон', 'Зеленый газон', 500, 20)"

    assert captured.out.strip() == expected
    assert repr(grass) == expected


def test_average_price():
    products = [
        Product("Товар 1", "Описание", 100, 1),
        Product("Товар 2", "Описание", 200, 1),
    ]
    category = Category("Категория", "Описание", products)

    assert category.average_price() == 150


def test_average_price_of_empty_category():
    category = Category("Категория", "Описание", [])

    assert category.average_price() == 0


def test_product_with_zero_quantity():
    with pytest.raises(
        ValueError,
        match="Товар с нулевым количеством не может быть добавлен",
    ):
        Product("Товар", "Описание", 100, 0)