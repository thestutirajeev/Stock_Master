import json

class Product:
    #Initializes product details ( Constructor )
    def __init__(self, product_id, name, price, quantity, category, img, description):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.img = img
        self.description = description

    #Converts Product object to dictionary (for saving to JSON)
    def to_dict(self):
        """Convert product object to dictionary (for saving to JSON)."""
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "img": self.img,
            "description": self.description
        }

    #Creates a Product object from dictionary data (when loading from JSON)
    @staticmethod
    def from_dict(product_id, data):
        """Create a Product object from dictionary data."""
        return Product(
            product_id, 
            data["name"], 
            data["price"], 
            data["quantity"], 
            data["category"], 
            data["img"], 
            data["description"]
        )

    #Loads products from JSON and returns a dictionary of Product objects
    @staticmethod
    def load_products():
        """Load products from JSON and return a dictionary of Product objects."""
        PRODUCTS_FILE = "database/products.json"
        try:
            with open(PRODUCTS_FILE, "r") as file:
                data = json.load(file)
            return {pid: Product.from_dict(pid, pdata) for pid, pdata in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}