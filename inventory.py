from models.product import Product
'''
# Load products
inventory = Product.load_products()

# Print loaded products
print("📦 Loaded Products:")
for pid, product in inventory.items():
    print(f"{pid} -> {product.name}, ₹{product.price}, Quantity: {product.quantity}")

# Add a new product
success, message = Product.add_product("P10P5", "Keyboard", 1500, 30, "Electronics", "images/keyboard.jpg", "Wireless Keyboard")

# Print result
print("✅" if success else "❌", message)
"""
# Test update product
success, message = Product.update_product("P103", price=1800, quantity=25)

# Print result
print("✅" if success else "❌", message)

# Test delete product
success, message = Product.delete_product("P105")

# Print result
print("✅" if success else "❌", message)

# Search by keyword (matches substring in name, category, description)
products = Product.search_products(keyword="top")
# Finds: "Laptop", "Tabletopper", "Topper" etc.

# Search by Product ID
products = Product.search_products(product_id="P101")

# Search by price range (only min limit)
products = Product.search_products(price_range=(5000, None))  # Min price 5000+

# Search by price range (only max limit)
products = Product.search_products(price_range=(None, 10000))  # Max price 10000

print("🔍 Search Results:")
# Search by quantity range (both limits)
products = Product.search_products(quantity_range=(5, 30))

# Show results
if products:
    for p in products:
        print("✅ Found:", p.to_dict())
else:
    print("❌ No matching products found.")
'''
'''
# Service

from services.stock_management import check_stock_levels

low_stock = check_stock_levels(3)  # Check for products below 3 units
if low_stock:
    print("⚠️ Low Stock Alert:", low_stock)
else:
    print("✅ Sufficient stock levels.")

# Service - Refill Stock
from services.stock_management import refill_stock
res = refill_stock("P104", 10)  # Refill 10 units of product P104
print(res)

from services.sales import sell_products

# Selling multiple products
result = sell_products([
    ("P103", 5),  # 2 Keyboards
    ("P101", 5)   # 1 Mouse
], "Rajeev Singh", "9876543210")

print(result)
'''
from services.reports import get_best_selling_products, get_total_revenue, get_sales_history

print("📌 \nBest-Selling Products:")
print(get_best_selling_products(7))  # Best-selling products in the last 7 days

print("\n\n📌 Total Revenue:")
print(get_total_revenue(30))

print("\n\n📌 Sales History:")
print(get_sales_history(1))


