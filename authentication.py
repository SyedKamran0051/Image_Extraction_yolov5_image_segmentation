import jwt
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")

def jwt_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        try:
            token = token.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

def extract_username_from_jwt(token):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Extract the username from the payload
        username = payload['sub']
        
        return username
    
    except jwt.ExpiredSignatureError:
        return "Signature has expired"
    
    except jwt.InvalidTokenError:
        return "Invalid token"