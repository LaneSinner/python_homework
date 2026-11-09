class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity


    @classmethod
    def new_product(cls,product_data:dict) :
        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"]
        )

    @property
    def price(self):
       return self.__price
    @price.setter
    def price(self,new_price:float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented

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

    def add_product(self, product: Product)-> None:
        self.__products.append(product)
        Category.product_count+=1

    @property
    def products(self):
        product_str = ""
        for product in self.__products:
            product_str += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return product_str


    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
