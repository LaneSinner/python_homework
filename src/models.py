from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self):
        pass


class MixinLog:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))


    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name!r}, {self.description!r}, "
            f"{self.price}, {self.quantity})"
        )


class Product(MixinLog, BaseProduct):
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.quantity = quantity
        super().__init__()


    @classmethod
    def new_product(cls, product_data: dict):
        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented

        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать товары разных классов:"
                f"{type(self).__name__} и {type(other).__name__}"
            )

        self_sum = self.price * self.quantity
        other_sum = other.price * other.quantity
        return self_sum + other_sum

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class Category:
    name: str
    description: str
    products: list

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только продукты")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        product_str = ""
        for product in self.__products:
            product_str += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return product_str

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


    def average_price(self):
        try:
            return sum(product.price for product in self.__products) / len(self.__products)
        except ZeroDivisionError:
            return 0


class Smartphone(Product):
    efficiency: str
    model: str
    memory: int
    color: str

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: str,
            model: str,
            memory: int,
            color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    country: str
    germination_period: str
    color: str

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: str,
            color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

product = Product("Продукт1", "Описание продукта", 1200, 10)