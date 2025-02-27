from models.product import Product

# Load products
inventory = Product.load_products()

# Print loaded products (for testing)
print("📦 Loaded Products:")
for pid, product in inventory.items():
    print(f"{pid} -> {product.name}, ₹{product.price}, Quantity: {product.quantity}")
