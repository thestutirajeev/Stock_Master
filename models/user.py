import json
import bcrypt  # Use bcrypt for secure password hashing

USERS_FILE = "database/users.json"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Store the already hashed password
        self.role = role  # "admin" or "employee"

    @staticmethod
    def hash_password(password):
        """Hash the password using bcrypt for security."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()  # Store as a string

    @staticmethod
    def verify_password(password, hashed_password):
        if not hashed_password.startswith("$2b$"):  # Check for valid bcrypt format
            return False
        """Verify password against the stored hashed version."""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def load_users():
        """Load all users from JSON file and format them correctly."""
        try:
            with open(USERS_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def save_users(users):
        """Save users to JSON file."""
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)

    @classmethod
    def authenticate(cls, username, password):
        """Check if the username and password match a stored user."""
        users = cls.load_users()
        if username in users and cls.verify_password(password, users[username]["password"]):
            return cls(username, users[username]["password"], users[username]["role"])  # Return user object
        return None  # Authentication failed

    @classmethod
    def add_user(cls, username, password, role):
        """Add a new user (only for admin)."""
        users = cls.load_users()
        if username in users:
            return False  # User already exists
        users[username] = {"password": cls.hash_password(password), "role": role}
        cls.save_users(users)
        return True  # User successfully added
