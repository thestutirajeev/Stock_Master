from authentication import Auth
from models.product import Product
from models.user import User 
from services.reports import get_best_selling_products, get_total_revenue, get_sales_history
from services.sales import sell_products
from services.stock_management import check_stock_levels, refill_stock
from models.product import Product

# Helper function to get optional input (returns None if empty)
def get_optional_input(prompt, cast_func=None):
    val = input(prompt)
    if val.strip() == "":
        return None
    if cast_func:
        try:
            return cast_func(val)
        except Exception:
            print("⚠️ Invalid input, ignoring.")
            return None
    return val

def product_tab():
    while True:
        print(
            "\n📋 Admin Panel:\n"
            "1. View Products 📦\n"
            "2. Add Product ➕\n"
            "3. Update Product ✏️\n"
            "4. Delete Product ❌\n"
            "5. Search Products 🔍\n"
            "6. Check Stock Levels ⚠️\n"
            "7. 🔙 Return to Admin Panel 👋"
        )

        choice = input("👉 Choose an option: ")

        if choice == "1":
            # View Products
            products = Product.load_products()
            if products:
                print("📦 All Products:")
                for pid, prod in products.items():
                    print(f"🔹 {pid}: {prod.name}, ₹{prod.price}, Qty: {prod.quantity}")
            else:
                print("⚠️ No products found.")

        elif choice == "2":
            # Add Product
            pid = input("👉 Enter Product ID: ").strip()
            name = input("👉 Enter Name: ").strip()
            price_input = input("👉 Enter Price: ").strip()
            quantity_input = input("👉 Enter Quantity: ").strip()
            category = input("👉 Enter Category: ").strip()
            image = input("👉 Enter Image Path: ").strip()
            desc = input("👉 Enter Description: ").strip()

            # Check if any required field is missing
            if not (pid and name and price_input and quantity_input and category and image and desc):
                print("⚠️ All fields are required!")
            else:
                try:
                    price = float(price_input)
                    quantity = int(quantity_input)
                    success, message = Product.add_product(pid, name, price, quantity, category, image, desc)
                    print("✅" if success else "❌", message)
                except ValueError:
                    print("⚠️ Price must be a number and Quantity must be an integer!")

        elif choice == "3":
            # Update Product
            pid = input("👉 Enter Product ID to update: ")
            print("👉 Enter new details (press Enter to skip any field):")
            new_name = input("   New Name: ")
            new_price = get_optional_input("   New Price: ", float)
            new_quantity = get_optional_input("   New Quantity: ", int)
            new_category = input("   New Category: ")
            new_image = input("   New Image Path: ")
            new_desc = input("   New Description: ")
            # Convert empty strings to None
            new_name = new_name if new_name.strip() != "" else None
            new_category = new_category if new_category.strip() != "" else None
            new_image = new_image if new_image.strip() != "" else None
            new_desc = new_desc if new_desc.strip() != "" else None

            if (new_name is None and new_price is None and new_quantity is None and 
                new_category is None and new_image is None and new_desc is None):
                print("⚠️ At least one field must be entered to update.")
            else:
                success, message = Product.update_product(
                    pid,
                    name=new_name,
                    price=new_price,
                    quantity=new_quantity,
                    category=new_category,
                    img=new_image,
                    description=new_desc
                )
                print("✅" if success else "❌", message)

        elif choice == "4":
            # Delete Product
            pid = input("👉 Enter Product ID to delete: ")
            success, message = Product.delete_product(pid)
            print("✅" if success else "❌", message)

        elif choice == "5":
            # Search Products
            print("👉 Enter search criteria (leave blank to skip):")
            search_pid = input("   Product ID (exact match): ")
            keyword = input("   Keyword (in name, category, description): ")

            lower_price = get_optional_input("   Lower Price Limit: ", float)
            upper_price = get_optional_input("   Upper Price Limit: ", float)
            if lower_price is None and upper_price is None:
                price_range = None
            else:
                price_range = (lower_price, upper_price)

            lower_qty = get_optional_input("   Lower Quantity Limit: ", int)
            upper_qty = get_optional_input("   Upper Quantity Limit: ", int)
            if lower_qty is None and upper_qty is None:
                quantity_range = None
            else:
                quantity_range = (lower_qty, upper_qty)

            results = Product.search_products(
                product_id=search_pid if search_pid.strip() != "" else None,
                price_range=price_range,
                quantity_range=quantity_range,
                keyword=keyword if keyword.strip() != "" else None
            )
            if results:
                print("🔍 Search Results:")
                for prod in results:
                    print(f"🔹 {prod.product_id}: {prod.name}, ₹{prod.price}, Qty: {prod.quantity}")
            else:
                print("⚠️ No matching products found.")

        elif choice == "6":
            # Check Stock Levels
            threshold = get_optional_input("👉 Enter stock threshold: ", int)
            if threshold is None:
                threshold = 5
            low_stock = check_stock_levels(threshold)
            if low_stock:
                print("⚠️ Low Stock Alert:")
                for item in low_stock:
                    print(f"🔹 {item['product_id']}: {item['name']}, Qty: {item['quantity']}")
            else:
                print("✅ Stock levels are sufficient.")

        elif choice == "7":
            print("🔙 Returning to Admin Panel...")
            return

        else:
            print("⚠️ Invalid option. Please try again.")

def user_tab():
    while True:
        print("\n👤 User Management")
        print("1️⃣ Load Users")
        print("2️⃣ Add User")
        print("3️⃣ 🔙 Back to Admin Panel")

        choice = input("👉 Choose an option: ")

        match choice:
            case "1":
                users = User.load_users()
                if users:
                    print("\n📜 Registered Users:")
                    for username, details in users.items():
                        print(f"   🆔 Username: {username} | 🔑 Role: {details['role']}")
                else:
                    print("⚠️ No users found!")

            case "2":
                username = input("👉 Enter New Username: ")
                password = input("🔑 Enter Password: ")
                role = input("🎭 Enter Role (admin/employee): ").lower()

                if role not in ["admin", "employee"]:
                    print("⚠️ Invalid role! Please enter 'admin' or 'employee'.")
                    continue

                success = User.add_user(username, password, role)
                print("✅ User added successfully!" if success else "❌ Username already exists!")

            case "3":
                print("🔙 Returning to Admin Panel...")
                return

            case _:
                print("⚠️ Invalid choice. Please try again.")

def reports_tab():
    while True:
        print("\n📊 Reports Panel")
        print("1️⃣ View Best-Selling Products")
        print("2️⃣ View Total Revenue")
        print("3️⃣ View Sales History")
        print("4️⃣ 🔙 Back to Admin Panel")

        choice = input("👉 Choose an option: ")

        match choice:
            case "1":
                days = input("📅 Enter number of days (or press Enter for all time): ")
                days = int(days) if days.strip().isdigit() else None
                result = get_best_selling_products(days)

                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"\n📅 Sales Report ({result['start_date']} - {result['end_date']})")
                    if result["best_sellers"]:
                        print("🏆 Best-Selling Products:")
                        for item in result["best_sellers"]:
                            print(f"   🔹 {item['name']} (ID: {item['product_id']}) - {item['sold']} units sold")
                    else:
                        print("⚠️ No sales data available.")

            case "2":
                days = input("📅 Enter number of days (or press Enter for all time): ")
                days = int(days) if days.strip().isdigit() else None
                result = get_total_revenue(days)

                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"\n💰 Total Revenue Report ({result['start_date']} - {result['end_date']})")
                    print(f"💵 Total Revenue: ₹{result['total_revenue']:.2f}")

            case "3":
                days = input("📅 Enter number of days (or press Enter for all time): ")
                days = int(days) if days.strip().isdigit() else None
                result = get_sales_history(days)

                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"\n📅 Sales History ({result['start_date']} - {result['end_date']})")
                    if result["transactions"]:
                        print("📜 Transactions:")
                        for txn in result["transactions"]:
                            print(f"   📅 Date: {txn['date']} | 🆔 Transaction ID: {txn['transaction_id']} | 💰 Amount: ₹{txn['total_price']:.2f}")
                    else:
                        print("⚠️ No sales history available.")

            case "4":
                print("🔙 Returning to Admin Panel...")
                break

            case _:
                print("⚠️ Invalid choice. Please try again.")

def sales_tab():
    while True:
        print("\n🛒 Sales Panel")
        print("1️⃣ Sell Products")
        print("2️⃣ 🔙 Back to Admin Panel")

        choice = input("👉 Choose an option: ")

        match choice:
            case "1":
                product_details = []
                while True:
                    product_id = input("🆔 Enter Product ID (or press Enter to finish): ").strip()
                    if not product_id:
                        break
                    quantity = input("📦 Enter Quantity: ").strip()
                    
                    if not quantity.isdigit() or int(quantity) <= 0:
                        print("⚠️ Invalid quantity. Please enter a valid number.")
                        continue

                    product_details.append((product_id, int(quantity)))

                if not product_details:
                    print("⚠️ No products selected for sale.")
                    continue

                customer_name = input("👤 Enter Customer Name: ").strip()
                customer_phone = input("📞 Enter Customer Phone: ").strip()

                result = sell_products(product_details, customer_name, customer_phone)

                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print("\n✅ Transaction Successful!")
                    print(f"🆔 Transaction ID: {result['transaction_id']}")
                    print(f"💰 Total Price: ₹{result['total_price']:.2f}")
                    print("📜 Sold Items:")
                    for item in result["sold_items"]:
                        print(f"   🔹 Product ID: {item['product_id']} | 📦 Quantity: {item['quantity']} | 💵 Price: ₹{item['price']:.2f}")

            case "2":
                print("🔙 Returning to Admin Panel...")
                break

            case _:
                print("⚠️ Invalid choice. Please try again.")

def stock_tab():
    while True:
        print("\n📦 Stock Management")
        print("1️⃣ Check Low Stock Products")
        print("2️⃣ Refill Stock")
        print("3️⃣ 🔙 Back to Admin Panel")

        choice = input("👉 Choose an option: ")

        match choice:
            case "1":
                threshold = input("⚠️ Enter stock threshold (default = 5): ").strip()
                threshold = int(threshold) if threshold.isdigit() else 5

                low_stock_items = check_stock_levels(threshold)

                if "error" in low_stock_items:
                    print(f"❌ {low_stock_items['error']}")
                elif not low_stock_items:
                    print("✅ All products have sufficient stock! 🎉")
                else:
                    print("\n⚠️ Low Stock Products:")
                    for item in low_stock_items:
                        print(f"   🔹 {item['name']} (🆔 {item['product_id']}) - Only {item['quantity']} left!")

            case "2":
                product_id = input("🆔 Enter Product ID to refill: ").strip()
                quantity = input("📦 Enter quantity to add: ").strip()

                if not quantity.isdigit() or int(quantity) <= 0:
                    print("⚠️ Invalid quantity. Please enter a valid number.")
                    continue

                result = refill_stock(product_id, int(quantity))

                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"✅ {result['message']}")

            case "3":
                print("🔙 Returning to Admin Panel...")
                break

            case _:
                print("⚠️ Invalid choice. Please try again.")

def admin_panel():
    while True:
        print("\n📋 Admin Panel")
        print("1️⃣ Product Tab")
        print("2️⃣ User Tab")
        print("3️⃣ Reports Tab")
        print("4️⃣ Sales Tab")
        print("5️⃣ Stock Tab")
        print("6️⃣ 🚪 Logout")

        choice = input("👉 Choose an option: ")

        match choice:
            case "1":
                product_tab()  # Handles Product-related tasks
            case "2":
                user_tab()  # Handles User Management
            case "3":
                reports_tab()  # Handles Reports
            case "4":
                sales_tab()  # Handles Sales
            case "5":
                stock_tab()  # Handles Stock Management
            case "6":
                # Logout
                from authentication import Auth  # Ensure correct import if needed
                Auth.logout()
                print("👋 Logged out successfully!")
                return
            case _:
                print("⚠️ Invalid choice. Please try again.")

def employee_panel():
    while True:
        print(
            "\n👤 Employee Panel:\n"
            "1. View Products 📦\n"
            "2. Search Products 🔍\n"
            "3. Best Selling Products 🔝\n"
            "4. Sell Products 💳\n"
            "5. Check Stock Levels ⚠️\n"
            "6. Refill Stock 🔄\n"
            "7. Logout 👋"
        )
        
        choice = input("👉 Choose an option: ")

        if choice == "1":
            # View Products
            products = Product.load_products()
            if products:
                print("📦 All Products:")
                for pid, prod in products.items():
                    print(f"🔹 {pid}: {prod.name}, ₹{prod.price}, Qty: {prod.quantity}")
            else:
                print("⚠️ No products found.")

        elif choice == "2":
            # Search Products
            print("🔍 Search Products")
            search_pid = input("   Product ID (exact match): ")
            keyword = input("   Keyword (name, category, description): ")
            lower_price = get_optional_input("   Lower Price Limit: ", float)
            upper_price = get_optional_input("   Upper Price Limit: ", float)
            lower_qty = get_optional_input("   Lower Quantity Limit: ", int)
            upper_qty = get_optional_input("   Upper Quantity Limit: ", int)

            price_range = (lower_price, upper_price) if (lower_price or upper_price) else None
            quantity_range = (lower_qty, upper_qty) if (lower_qty or upper_qty) else None

            results = Product.search_products(
                product_id=search_pid if search_pid.strip() != "" else None,
                price_range=price_range,
                quantity_range=quantity_range,
                keyword=keyword if keyword.strip() != "" else None
            )

            if results:
                print("✅ Search Results:")
                for prod in results:
                    print(f"🔹 {prod.product_id}: {prod.name}, ₹{prod.price}, Qty: {prod.quantity}")
            else:
                print("⚠️ No matching products found.")

        elif choice == "3":
            # Best Selling Products
            days = get_optional_input("👉 Enter days to filter (Leave blank for all time): ", int)
            report = get_best_selling_products(days)
            if report["best_sellers"]:
                print(f"🔝 Best-Selling Products from {report['start_date']} to {report['end_date']}:")
                for item in report["best_sellers"]:
                    print(f"🔹 {item['product_id']}: {item['name']}, Sold: {item['sold']}")
            else:
                print("⚠️ No sales data available.")

        elif choice == "4":
            # Sell Products
            print("💳 Sell Products")
            product_details = []
            while True:
                pid = input("👉 Enter Product ID (or press Enter to finish): ")
                if pid.strip() == "":
                    break
                quantity = get_optional_input("   Quantity: ", int)
                if quantity:
                    product_details.append((pid, quantity))

            if not product_details:
                print("⚠️ No products selected.")
                continue

            customer_name = input("👉 Customer Name: ")
            customer_phone = input("👉 Customer Phone: ")

            result = sell_products(product_details, customer_name, customer_phone)
            if "error" in result:
                print("❌", result["error"])
            else:
                print("✅ Transaction Successful!")
                print(f"🆔 Transaction ID: {result['transaction_id']}")
                print(f"💰 Total Price: ₹{result['total_price']}")

        elif choice == "5":
            # Check Stock Levels
            threshold = get_optional_input("👉 Enter Stock Threshold: ", int) or 5
            low_stock = check_stock_levels(threshold)
            if low_stock:
                print("⚠️ Low Stock Items:")
                for item in low_stock:
                    print(f"🔹 {item['product_id']}: {item['name']}, Qty: {item['quantity']}")
            else:
                print("✅ All stock levels are sufficient.")

        elif choice == "6":
            # Refill Stock
            pid = input("👉 Enter Product ID: ")
            quantity = get_optional_input("   Quantity to Refill: ", int)
            if quantity:
                result = refill_stock(pid, quantity)
                print("✅" if "message" in result else "❌", result.get("message", result.get("error")))

        elif choice == "7":
            # Logout
            Auth.logout()
            print("👋 Logged out successfully!")
            break

        else:
            print("⚠️ Invalid option. Please try again.")


# Main App
username = input("Username: ")
password = input("Password: ")

if Auth.login(username, password):
    if Auth.is_admin():
        admin_panel()
    elif Auth.is_employee():
        employee_panel()
else:
    print("Invalid login!")
