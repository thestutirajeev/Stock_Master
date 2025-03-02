import json
import os
from datetime import datetime

class Transaction:
    def __init__(self, transaction_id, product_ids, quantities, prices, customer_name, customer_phone, date=None):
        self.transaction_id = transaction_id
        self.product_ids = product_ids
        self.quantities = quantities
        self.prices = prices
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Convert transaction object to dictionary for JSON storage."""
        return {
            "transaction_id": self.transaction_id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "product_ids": self.product_ids,
            "quantities": self.quantities,
            "prices": self.prices,
            "date": self.date
        }

    @staticmethod
    def from_dict(transaction_id, data):
        """Convert dictionary data back to a Transaction object."""
        return Transaction(
            transaction_id=transaction_id,
            customer_name=data["customer_name"],
            customer_phone=data["customer_phone"],
            product_ids=data["product_ids"],
            quantities=data["quantities"],
            prices=data["prices"],
            date=data.get("date")  # Use existing date if available
        )

    @staticmethod
    def load_transactions():
        """Load all transactions from JSON with proper object conversion."""
        TRANSACTIONS_FILE = "database/transactions.json"

        try:
            with open(TRANSACTIONS_FILE, "r") as file:
                data = json.load(file)
            return {tid: Transaction.from_dict(tid, tdata) for tid, tdata in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_transactions(transactions):
        """Save all transactions to JSON."""
        with open("database/transactions.json", "w") as file:
            json.dump(
                {tid: (t.to_dict() if isinstance(t, Transaction) else t) for tid, t in transactions.items()},
                file,
                indent=4
            )
