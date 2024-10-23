from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User:
    @staticmethod
    def create_user(username, password, role='user'):
        user_data = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "role": role
        }
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)  # Return the ID of the inserted document

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def check_password(stored_hash, password):
        return check_password_hash(stored_hash, password)
