from flask import Blueprint, request, jsonify
from services.login_service import LoginService
from constants import DB_name,path
#buleprint and service
login_blueprint = Blueprint('login', __name__)
login_service = LoginService(path)

@login_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
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
def create_user():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        login_service.create_user(username, password)
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