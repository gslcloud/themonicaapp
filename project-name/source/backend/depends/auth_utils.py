import bcrypt
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class UserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, username: str, password: str) -> None:
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        if username in self.users:
            raise ValueError("Username already exists.")

        user = User(username, password)
        self.users[username] = user

    def get_user_by_username(self, username: str) -> User:
        if username not in self.users:
            raise ValueError("User not found.")

        return self.users[username]