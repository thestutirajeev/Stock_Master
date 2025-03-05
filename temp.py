import json
import bcrypt

users_file = "database/users.json"

# Load users
with open(users_file, "r") as f:
    users = json.load(f)

# Rehash plain text passwords
for username, details in users.items():
    if not details["password"].startswith("$2b$"):  # If password is not hashed
        hashed_password = bcrypt.hashpw(details["password"].encode(), bcrypt.gensalt()).decode()
        users[username]["password"] = hashed_password

# Save updated users.json
with open(users_file, "w") as f:
    json.dump(users, f, indent=4)

print("✅ Passwords updated successfully.")
