from models.product import Product

def check_stock_levels(threshold=5):
    """Checks stock levels and returns a list of low-stock items."""
    products = Product.load_products()  # It returns a dict of Product objects
    low_stock_items = [
        {"product_id": product.product_id, "name": product.name, "quantity": product.quantity}
        for product in products.values() if product.quantity < threshold
    ]
    
    return low_stock_items  # Returns a list of low-stock items


def refill_stock(product_id, quantity):
    """Increases stock of a specific product using update_product."""
    if quantity <= 0:
        return {"error": "Quantity must be greater than zero."}

    # Load products to check if the product exists
    products = Product.load_products()
    if product_id not in products:
        return {"error": f"Product ID {product_id} not found."}

    # Get the current stock and update it
    current_quantity = products[product_id].quantity
    new_quantity = current_quantity + quantity

    # Use existing update_product method to update the quantity
    success, message = Product.update_product(product_id, quantity=new_quantity)

    if success:
        return {"message": f"Stock refilled successfully. New quantity: {new_quantity}"}
    else:
        return {"error": message}
