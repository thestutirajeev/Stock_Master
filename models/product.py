import json
import re
from authentication import Auth

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
            "product_id": self.product_id,
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
        """Login Required"""
        if not Auth.get_logged_in_user():
            return {"error": "Access denied. Login required."}
        PRODUCTS_FILE = "database/products.json"
        try:
            with open(PRODUCTS_FILE, "r") as file:
                data = json.load(file)
            return {pid: Product.from_dict(pid, pdata) for pid, pdata in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    #Adds a new product and saves to JSON
    @staticmethod
    def add_product(product_id, name, price, quantity, category, img, description):
        """Only admins can add products."""
        if not Auth.is_admin():
            return {"error": "Access denied. Admins only."}
        
        
        """Add a new product after validation and save to JSON."""
        PRODUCTS_FILE = "database/products.json"

        # Validate inputs before proceeding
        is_valid, error_message = Product.validate_product_data(product_id, name, price, quantity, category, img, description)
        if not is_valid:
            return False, error_message

        # Load existing products
        products = Product.load_products()

        # Check if product ID already exists
        if product_id in products:
            return False, "Product ID already exists!"

        # Create new product object
        new_product = Product(product_id, name, price, quantity, category, img, description)
        products[product_id] = new_product

        # Save updated products to JSON
        with open(PRODUCTS_FILE, "w") as file:
            json.dump({pid: prod.to_dict() for pid, prod in products.items()}, file, indent=4)

        return True, "Product added successfully!"

    #Validates product data before adding to inventory
    @staticmethod
    def validate_product_data(product_id, name, price, quantity, category, img, description):
        """Validate product inputs before adding to inventory."""

        # Validate product ID format (P101, P102, etc.)
        if not re.match(r"^P\d{3}$", product_id):
            return False, "Invalid Product ID! Use format: P101"

        # Validate name, category, and description (non-empty)
        if not all(isinstance(value, str) and value.strip() for value in [name, category, description]):
            return False, "Name, category, and description cannot be empty!"

        # Validate price and quantity (must be positive numbers)
        if not (isinstance(price, (int, float)) and price > 0):
            return False, "Price must be a positive number!"
        if not (isinstance(quantity, int) and quantity >= 0):
            return False, "Quantity must be a non-negative integer!"

        return True, ""  # No error

    #Updates product details in the inventory
    @staticmethod
    def update_product(product_id, name=None, price=None, quantity=None, category=None, img=None, description=None):
        """Only admins can add products."""
        if not Auth.is_admin():
            return {"error": "Access denied. Admins only."}
        
        
        """Update product details in the inventory."""

        # Load products
        products = Product.load_products()

        # Check if product exists
        if product_id not in products:
            return False, "❌ Product ID not found!"

        # Get existing product
        product = products[product_id]

        # Prepare updated values (keep existing values if None)
        updated_data = {
            "product_id": product_id,  # Required for validation
            "name": name if name is not None else product.name,
            "price": price if price is not None else product.price,
            "quantity": quantity if quantity is not None else product.quantity,
            "category": category if category is not None else product.category,
            "img": img if img is not None else product.img,
            "description": description if description is not None else product.description,
        }

        # Validate updated data using existing function
        is_valid, error_message = Product.validate_product_data(**updated_data)
        if not is_valid:
            return False, error_message

        # Apply updates
        product.name = updated_data["name"]
        product.price = updated_data["price"]
        product.quantity = updated_data["quantity"]
        product.category = updated_data["category"]
        product.img = updated_data["img"]
        product.description = updated_data["description"]

        # Save updated products to JSON
        with open("database/products.json", "w") as file:
            json.dump({pid: prod.to_dict() for pid, prod in products.items()}, file, indent=4)

        return True, "✅ Product updated successfully!"

    #Deletes a product from the inventory
    @staticmethod
    def delete_product(product_id):
        """Only admins can add products."""
        if not Auth.is_admin():
            return {"error": "Access denied. Admins only."}
        
        """Delete a product from the inventory."""
        
        # Load existing products
        products = Product.load_products()

        # Check if product exists
        if product_id not in products:
            return False, "❌ Product ID not found!"

        # Remove product
        del products[product_id]

        # Save updated products to JSON
        with open("database/products.json", "w") as file:
            json.dump({pid: prod.to_dict() for pid, prod in products.items()}, file, indent=4)

        return True, "✅ Product deleted successfully!"
    
    # All Search Functions

    #Search for a product by its ID
    @staticmethod
    def search_by_id(product_id):
        """Search for a product by its ID."""
        products = Product.load_products()
        
        return products.get(product_id, None)

    @staticmethod
    def search_products(product_id=None, price_range=None, quantity_range=None, keyword=None):
        """
        Search products based on multiple filters.
        
        - product_id: Exact match (e.g., "P101").
        - keyword: Substring match in name, category, or description (case-insensitive).
        - price_range: Tuple (min_price, max_price) - either can be None.
        - quantity_range: Tuple (min_qty, max_qty) - either can be None.
        """
        if not Auth.get_logged_in_user():
            return {"error": "Access denied. Login required."}
        products = Product.load_products()
        results = []

        for product in products.values():
            match = True

            # Search by Product ID (exact match)
            if product_id and product.product_id != product_id:
                match = False

            # Search by keyword (substring in name, category, or description)
            if keyword:
                keyword_lower = keyword.lower()
                fields_to_search = [product.name, product.category, product.description]
                if not any(keyword_lower in field.lower() for field in fields_to_search):
                    match = False

            # Search by price range (supports only lower or upper limit too)
            if price_range:
                min_price, max_price = price_range
                if min_price is not None and product.price < min_price:
                    match = False
                if max_price is not None and product.price > max_price:
                    match = False

            # Search by quantity range (supports only lower or upper limit too)
            if quantity_range:
                min_qty, max_qty = quantity_range
                if min_qty is not None and product.quantity < min_qty:
                    match = False
                if max_qty is not None and product.quantity > max_qty:
                    match = False

            if match:
                results.append(product)

        return results
