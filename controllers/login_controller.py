from flask import Blueprint, request, jsonify
from services.login_service import LoginService

login_blueprint = Blueprint('login', __name__)
login_service = LoginService('/mnt/data/image_extraction_project.db')

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
