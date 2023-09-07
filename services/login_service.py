import jwt
from database_connection import DatabaseConnection
import os
from werkzeug.security import check_password_hash
from models.user import User
from datetime import datetime,timedelta
from init_db import db


SECRET_KEY = os.getenv("SECRET_KEY") # This should be a secure random value in a real application

class LoginService:
    def __init__(self, db_path):
        self.db_path = db_path

    def auth(self, username):
        user = User.query.filter_by(username=username).first()  # Assuming a query method in User class
        if user:
            return {"username": user.username, "password": user.password}
        else:
            return None 
        
    def authenticate_user(self, username, password):
        # Check credentials against database
        db = DatabaseConnection(self.db_path)
        try:
            cursor = db.connect()
        except Exception as e:
            return e
        user = self.auth(username)

        db.close()
        if user and check_password_hash(user['password'], password):
            # If user exists, create a JWT token
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user["username"] 
            }
            token = jwt.encode(payload, SECRET_KEY)
            return {"message": "Login successful", "token": token, "username": user["username"]}
        else:
            return {"message": "Invalid credentials"}
    

    def create_user(self,username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()



    def delete_user(self,username):
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return 1
        else:
            return 0