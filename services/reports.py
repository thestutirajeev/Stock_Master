from collections import defaultdict
from models.transaction import Transaction
from models.product import Product
from models.auth import Auth
from datetime import datetime, timedelta

def filter_transactions_by_date(days=None):
    """Filter transactions within the last 'days' days. If None, return all."""
    transactions = transactions = Transaction.load_transactions()
    if days is None:  # No filter, return all transactions
        return transactions

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)  # Calculate start date

    filtered = {
        tid: txn for tid, txn in transactions.items()
        if start_date <= datetime.strptime(txn.date, "%Y-%m-%d %H:%M:%S") <= end_date
    }

    return filtered, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

# Get best-selling products
#determines the best-selling products based on the total quantity sold within the given time frame.
def get_best_selling_products(days=None):
    """Allow employees and admins to get best selling products."""
    if not Auth.get_logged_in_user():
        return {"error": "Please log in to get best selling products."}
    """Find best-selling products within the last 'days' days (default: all time)."""
    transactions, start_date, end_date = filter_transactions_by_date(days)

    sales_count = defaultdict(int)

    for transaction in transactions.values():
        for i, product_id in enumerate(transaction.product_ids):
            sales_count[product_id] += transaction.quantities[i]

    sorted_sales = sorted(sales_count.items(), key=lambda x: x[1], reverse=True)

    products = Product.load_products()
    report = [
        {"product_id": pid, "name": products[pid].name, "sold": count}
        for pid, count in sorted_sales
    ]

    return {"start_date": start_date, "end_date": end_date, "best_sellers": report}

# Get total revenue from all transactions
def get_total_revenue(days=None):
    """Allow only admins to get total revenue"""
    if not Auth.is_admin():
        return {"error": "Only Admin can to get total revenue."}

    """Calculate total revenue within the last 'days' days (default: all time)."""
    
    transactions, start_date, end_date = filter_transactions_by_date( days)

    total_revenue = sum(
        sum(transaction.quantities[i] * transaction.prices[i] for i in range(len(transaction.product_ids)))
        for transaction in transactions.values()
    )

    return {"start_date": start_date, "end_date": end_date, "total_revenue": total_revenue}

# Get sales history, sorted by date
def get_sales_history(days=None):
    """Allow admins to only."""
    if not Auth.is_admin():
        return {"error": "Access denied. Admins only."}
        
    """Return transactions sorted by date (newest first) for the last 'days' days."""
    transactions, start_date, end_date = filter_transactions_by_date( days)

    sorted_transactions = sorted(transactions.values(), key=lambda x: x.date, reverse=True)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "transactions": [t.to_dict() for t in sorted_transactions]
    }
