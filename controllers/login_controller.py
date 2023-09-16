from flask import Blueprint, request, jsonify
from authentication import extract_username_from_jwt
from services.login_service import LoginService
from werkzeug.security import generate_password_hash
from constants import DB_name,path
#buleprint and service
login_blueprint = Blueprint('login', __name__)
login_service = LoginService(path)

@login_blueprint.route('/login', methods=['POST'])
def login():
    print("login")
    try:
        data = request.json
        username = data.get("username")
        password = data.get('password')
        if not username or not password:
            return jsonify({"message": "Both username and password are required"}), 400
        
        # Use LoginService to authenticate user
        auth_result = login_service.authenticate_user(username, password)
        if 'token' in auth_result:
            return jsonify(auth_result), 200
        else:
            return jsonify(auth_result), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@login_blueprint.route('/create_user', methods=['POST'])
#@jwt_required() 
def create_user():
    try:

        data = request.get_json()
        username = data['username']
        password = data['password']
        
        hashed_password = generate_password_hash(password, method='scrypt',salt_length=10)
        login_service.create_user(username, hashed_password)
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@login_blueprint.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    flag = login_service.delete_user(username)
    if flag:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({"error": "User does not exist"}), 500
    
@login_blueprint.route('/change-password', methods=['POST'])
#@jwt_required()  # Ensures that the user is logged in
def change_password():
    try:
        data = request.json
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'message': 'Both old and new passwords are required'}), 400
        
        auth_header = request.headers.get('Authorization')
        bearer_token = auth_header.split(" ")[1]
        current_user = extract_username_from_jwt(bearer_token)

        if LoginService.change_password(current_user, old_password, new_password):
            return jsonify({'message': 'Password successfully changed'}), 200
        else:
            return jsonify({'message': 'Failed to change password. Please try again.'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred: ' + str(e)}), 500
