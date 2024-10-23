from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.models.user import User 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Find user by username in MongoDB
    user_data = User.find_by_username(data.get('username'))

    if user_data:
        # Check the password using the stored password hash
        if User.check_password(user_data['password_hash'], data.get('password')):
            access_token = create_access_token(identity=str(user_data['_id']))  # Use the user's MongoDB ID
            return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
