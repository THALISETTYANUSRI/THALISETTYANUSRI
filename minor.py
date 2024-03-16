import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.orders_placed = 0

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "orders_placed": self.orders_placed
        }

class Product:
    def __init__(self, name, price, category, stock):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock

class ECommerce:
    def __init__(self):
        self.load_users()
        self.load_orders()
        self.products = {}

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

    def load_orders(self):
        try:
            with open("orders.json", "r") as file:
                self.orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.orders = {}

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump({username: user.to_dict() for username, user in self.users.items()}, file)

    def save_orders(self):
        with open("orders.json", "w") as file:
            json.dump(self.orders, file)

    def register(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        else:
            self.users[username] = User(username, password)
            self.save_users()
            print("Registration successful!")
            return True

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False

    def add_product(self, name, price, category, stock):
        self.products[name] = Product(name, price, category, stock)

    def display_products(self):
        print("Products available:")
        for product in self.products.values():
            print(f"Name: {product.name}, Price: {product.price}, Category: {product.category}, Stock: {product.stock}")

    def place_order(self, username, product_name, quantity):
        if username not in self.users:
            print("User not registered.")
            return

        if product_name not in self.products:
            print("Product not found.")
            return

        product = self.products[product_name]
        if product.stock < quantity:
            print("Insufficient stock.")
            return

        # Update orders
        if username not in self.orders:
            self.orders[username] = []
        self.orders[username].append({"product_name": product_name, "quantity": quantity})

        # Update user's orders_placed
        if username in self.users:
            if 'orders_placed' not in self.users[username]:
                self.users[username]['orders_placed'] = 0
            self.users[username]['orders_placed'] += 1

        print("Order placed successfully!")
        print(f"Total amount: {product.price * quantity}")
        print("Complete the payment on delivery.")
        product.stock -= quantity

    def display_user_orders(self, username):
        if username in self.orders:
            print(f"Orders placed by {username}:")
            for order in self.orders[username]:
                print(f"Product: {order['product_name']}, Quantity: {order['quantity']}")
        else:
            print(f"No orders placed by {username}.")

def main():
    ecommerce = ECommerce()

    # Adding some products
    ecommerce.add_product("Laptop", 1000, "Electronics", 10)
    ecommerce.add_product("Smartphone", 500, "Electronics", 20)
    ecommerce.add_product("T-Shirt", 20, "Clothing", 50)
    ecommerce.add_product("Jeans", 50, "Clothing", 30)

    current_user = None

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Display Products")
        print("4. Place Order")
        print("5. Display User Orders")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if ecommerce.register(username, password):
                current_user = username

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if ecommerce.login(username, password):
                current_user = username

        elif choice == "3":
            if current_user:
                ecommerce.display_products()
            else:
                print("Please login first.")

        elif choice == "4":
            if not current_user:
                print("Please login first.")
            else:
                product_name = input("Enter product name: ")
                quantity = int(input("Enter quantity: "))
                ecommerce.place_order(current_user, product_name, quantity)

        elif choice == "5":
            if not current_user:
                print("Please login first.")
            else:
                ecommerce.display_user_orders(current_user)

        elif choice == "6":
            print("Exiting...")
            ecommerce.save_orders()  # Save orders before exiting
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
