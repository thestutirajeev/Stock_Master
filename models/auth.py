from models.user import User

class Auth:
    current_user = None  # Track logged-in user

    @staticmethod
    def login(username, password):
        """Log in a user by validating credentials."""
        user = User.authenticate(username, password)
        if user:
            Auth.current_user = user  # Store logged-in user
            return True
        return False

    @staticmethod
    def logout():
        """Log out the current user."""
        Auth.current_user = None

    @staticmethod
    def get_logged_in_user():
        """Return the currently logged-in user (if any)."""
        return Auth.current_user

    @staticmethod
    def is_admin():
        """Check if the logged-in user is an admin."""
        return Auth.current_user and Auth.current_user.role == "admin"

    @staticmethod
    def is_employee():
        """Check if the logged-in user is an employee."""
        return Auth.current_user and Auth.current_user.role == "employee"
