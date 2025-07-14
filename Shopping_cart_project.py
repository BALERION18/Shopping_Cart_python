import json
import os


class Product:
    def __init__(self, product_id: str, name: str, price: float, quantity_available: int):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_available = quantity_available

    @property
    def product_id(self): return self._product_id

    @property
    def name(self): return self._name

    @property
    def price(self): return self._price

    @property
    def quantity_available(self): return self._quantity_available

    @quantity_available.setter
    def quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value

    def decrease_quantity(self, amount: int) -> bool:
        if 0 < amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    def increase_quantity(self, amount: int):
        if amount > 0:
            self._quantity_available += amount

    def display_details(self) -> str:
        return f"[{self.product_id}] {self.name} - ₹{self.price:.2f}, In Stock: {self.quantity_available}"

    def to_dict(self) -> dict:
        return {
            "type": "base",
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity_available": self.quantity_available
        }

class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_available: int, weight: float):
        super().__init__(product_id, name, price, quantity_available)
        self._weight = weight

    @property
    def weight(self): return self._weight

    def display_details(self) -> str:
        return f"[{self.product_id}] {self.name} - ₹{self.price:.2f}, Weight: {self.weight}kg, Stock: {self.quantity_available}"

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({"type": "physical", "weight": self.weight})
        return base

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_available: int, download_link: str = "N/A"):
        super().__init__(product_id, name, price, quantity_available)
        self._download_link = download_link

    @property
    def download_link(self): return self._download_link

    def display_details(self) -> str:
        return f"[{self.product_id}] {self.name} - ₹{self.price:.2f} (Digital Product)"

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({"type": "digital"})
        return base


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = quantity

    @property
    def product(self): return self._product

    @property
    def quantity(self): return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value >= 0:
            self._quantity = value

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def __str__(self):
        return f"Item: {self.product.name}, Qty: {self.quantity}, Price: ₹{self.product.price:.2f}, Subtotal: ₹{self.calculate_subtotal():.2f}"

    def to_dict(self) -> dict:
        return {
            "product_id": self.product.product_id,
            "quantity": self.quantity
        }


class ShoppingCart:
    def __init__(self, product_catalog_file='products.json', cart_state_file='cart.json'):
        self._product_catalog_file = product_catalog_file
        self._cart_state_file = cart_state_file
        self._items = {}
        self._catalog = self._load_catalog()
        self._load_cart_state()

    def _load_catalog(self) -> dict:
        if not os.path.exists(self._product_catalog_file):
            self._generate_default_catalog()
        with open(self._product_catalog_file, 'r') as f:
            data = json.load(f)
        catalog = {}
        for item in data:
            ptype = item.get("type")
            if ptype == "physical":
                product = PhysicalProduct(item["product_id"], item["name"], item["price"], item["quantity_available"], item["weight"])
            elif ptype == "digital":
                product = DigitalProduct(item["product_id"], item["name"], item["price"], item["quantity_available"])
            else:
                product = Product(item["product_id"], item["name"], item["price"], item["quantity_available"])
            catalog[product.product_id] = product
        return catalog

    def _generate_default_catalog(self):
        items = [
            {"type": "physical", "product_id": "P001", "name": "Bluetooth Headphones", "price": 1599.00, "quantity_available": 10, "weight": 0.25},
            {"type": "physical", "product_id": "P002", "name": "Laptop Backpack", "price": 999.00, "quantity_available": 15, "weight": 1.0},
            {"type": "physical", "product_id": "P003", "name": "Water Bottle (1L)", "price": 299.00, "quantity_available": 25, "weight": 0.5},
            {"type": "physical", "product_id": "P004", "name": "Wireless Mouse", "price": 499.00, "quantity_available": 20, "weight": 0.15},
            {"type": "physical", "product_id": "P005", "name": "Notebook Set (Pack of 3)", "price": 199.00, "quantity_available": 30, "weight": 0.6},
            {"type": "digital", "product_id": "D001", "name": "E-Book: Learn Python", "price": 349.00, "quantity_available": 100},
            {"type": "digital", "product_id": "D002", "name": "E-Book: Data Structures", "price": 399.00, "quantity_available": 100},
            {"type": "digital", "product_id": "D003", "name": "Music Album (MP3)", "price": 249.00, "quantity_available": 200},
            {"type": "physical", "product_id": "P006", "name": "Power Bank (10000 mAh)", "price": 1299.00, "quantity_available": 18, "weight": 0.3},
            {"type": "physical", "product_id": "P007", "name": "USB Flash Drive (64GB)", "price": 549.00, "quantity_available": 40, "weight": 0.05},
            {"type": "physical", "product_id": "P008", "name": "Desk Organizer", "price": 349.00, "quantity_available": 22, "weight": 0.9},
            {"type": "digital", "product_id": "D004", "name": "Online Course: Java Programming", "price": 999.00, "quantity_available": 50},
            {"type": "physical", "product_id": "P009", "name": "Table Lamp (LED)", "price": 799.00, "quantity_available": 12, "weight": 1.2},
            {"type": "digital", "product_id": "D005", "name": "Stock Market Guide (PDF)", "price": 299.00, "quantity_available": 150},
            {"type": "physical", "product_id": "P010", "name": "Mobile Stand", "price": 149.00, "quantity_available": 35, "weight": 0.1},
            {"type": "physical", "product_id": "P011", "name": "Game of thrones", "price": 349.00, "quantity_available": 35, "weight": 1.5},
            {"type": "digital", "product_id": "P012", "name": "Hairdresser", "price": 799.00, "quantity_available": 35, "weight": 1.0}
            
        ]
        with open(self._product_catalog_file, 'w') as f:
            json.dump(items, f, indent=2)

    def _load_cart_state(self):
        if not os.path.exists(self._cart_state_file):
            return
        with open(self._cart_state_file, 'r') as f:
            data = json.load(f)
        for item in data:
            pid = item["product_id"]
            qty = item["quantity"]
            if pid in self._catalog:
                self._items[pid] = CartItem(self._catalog[pid], qty)

    def _save_catalog(self):
        data = [p.to_dict() for p in self._catalog.values()]
        with open(self._product_catalog_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _save_cart_state(self):
        data = [item.to_dict() for item in self._items.values()]
        with open(self._cart_state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def display_products(self):
        print("\n📦 Available Products:\n")
        for product in self._catalog.values():
            print(product.display_details())
        print()

    def display_cart(self):
        if not self._items:
            print("\n🛒 Cart is empty.\n")
            return
        print("\n🛒 Your Shopping Cart:\n")
        total = 0
        for item in self._items.values():
            print(item)
            total += item.calculate_subtotal()
        print(f"\nTotal Amount: ₹{total:.2f}\n")

    def add_item(self, product_id: str, quantity: int) -> bool:
        if product_id not in self._catalog:
            return False
        product = self._catalog[product_id]
        if not product.decrease_quantity(quantity):
            return False
        if product_id in self._items:
            self._items[product_id].quantity += quantity
        else:
            self._items[product_id] = CartItem(product, quantity)
        self._save_cart_state()
        return True

    def remove_item(self, product_id: str) -> bool:
        if product_id in self._items:
            item = self._items.pop(product_id)
            item.product.increase_quantity(item.quantity)
            self._save_cart_state()
            return True
        return False

    def update_quantity(self, product_id: str, new_quantity: int) -> bool:
        if product_id not in self._items or new_quantity < 0:
            return False
        item = self._items[product_id]
        diff = new_quantity - item.quantity
        if diff > 0:
            if not item.product.decrease_quantity(diff):
                return False
        else:
            item.product.increase_quantity(-diff)
        item.quantity = new_quantity
        if new_quantity == 0:
            self._items.pop(product_id)
        self._save_cart_state()
        return True

    def get_total(self) -> float:
        return sum(item.calculate_subtotal() for item in self._items.values())


def main():
    cart = ShoppingCart()
    while True:
        print("\n🛍️  Online Shopping Cart Menu")
        print("1. View Products")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Update Quantity in Cart")
        print("5. Remove Item from Cart")
        print("6. Checkout")
        print("7. Exit")
        choice = input("Enter choice (1-7): ")

        if choice == '1':
            cart.display_products()
        elif choice == '2':
            pid = input("Enter Product ID: ").strip()
            qty = int(input("Enter Quantity: "))
            if cart.add_item(pid, qty):
                print("✅ Item added to cart.")
            else:
                print("❌ Failed to add item.")
        elif choice == '3':
            cart.display_cart()
        elif choice == '4':
            pid = input("Enter Product ID to update: ").strip()
            qty = int(input("Enter new quantity: "))
            if cart.update_quantity(pid, qty):
                print("✅ Quantity updated.")
            else:
                print("❌ Failed to update.")
        elif choice == '5':
            pid = input("Enter Product ID to remove: ").strip()
            if cart.remove_item(pid):
                print("✅ Item removed.")
            else:
                print("❌ Item not found.")
        elif choice == '6':
            total = cart.get_total()
            print(f"\n💰 Checkout complete! Total amount: ₹{total:.2f}")
        elif choice == '7':
            cart._save_catalog()
            print("🛑 Exiting... Data saved.")
            break
        else:
            print("⚠️ Invalid option. Try again.")

if __name__ == "__main__":
    main()
