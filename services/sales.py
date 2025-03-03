from datetime import datetime
from models.product import Product
from models.transaction import Transaction
from models.auth import Auth

def generate_transaction_id(customer_name):
    """Generate a unique transaction ID based on date and customer initials."""
    timestamp = datetime.now().strftime("%y%m%d%H%M")  # YYMMDDHHMM
    initials = "".join([word[0] for word in customer_name.split()]).upper()  # Extract initials
    return f"{timestamp}_{initials}"  # Format: 2502281445_A

def sell_products(product_details, customer_name, customer_phone):
    """Allow employees and admins to sell products."""
    if not Auth.get_logged_in_user():
        return {"error": "Please log in to sell a product."}
    
    """
    Sell multiple products, decrease stock, and record transaction.
    
    product_details: List of tuples [(product_id, quantity), ...]
    customer_name: str
    customer_phone: str
    """
    if not product_details:
        return {"error": "No products selected for sale."}

    products = Product.load_products()
    product_ids = []
    quantities = []
    prices = []

    # Check stock availability
    for product_id, quantity in product_details:
        if product_id not in products:
            return {"error": f"Product {product_id} not found."}
        
        product = products[product_id]

        if quantity <= 0:
            return {"error": f"Invalid quantity for {product.name}."}
        
        if product.quantity < quantity:
            return {"error": f"Not enough stock for {product.name}."}

        product_ids.append(product_id)
        quantities.append(quantity)
        prices.append(product.price)

    # Deduct stock
    for i, product_id in enumerate(product_ids):
        new_quantity = products[product_id].quantity - quantities[i]
        Product.update_product(product_id, quantity=new_quantity)

    # Generate transaction ID dynamically
    transaction_id = generate_transaction_id(customer_name)

    # Create transaction
    transaction = Transaction(transaction_id, product_ids, quantities, prices, customer_name, customer_phone)

    transactions = Transaction.load_transactions()
    transactions[transaction_id] = transaction.to_dict()

    # Save transaction
    Transaction.save_transactions(transactions)

    total_price = sum(quantities[i] * prices[i] for i in range(len(product_ids)))

    return {
        "message": "Transaction successful!",
        "transaction_id": transaction_id,
        "total_price": total_price,
        "sold_items": [{"product_id": pid, "quantity": quantities[i], "price": prices[i]} for i, pid in enumerate(product_ids)]
    }
