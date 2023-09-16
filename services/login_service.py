import jwt
from database_connection import DatabaseConnection
import os
from werkzeug.security import generate_password_hash
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
        
    @staticmethod
    def change_password(current_user, old_password, new_password):
        # Fetch user by username (or ID, depending on your setup)
        user = User.query.filter_by(username=current_user).first()

        if user is None:
            return False

        # Verify the old password
        if not check_password_hash(user.password, old_password):
            return False

        # Hash the new password using scrypt
        hashed_new_password = generate_password_hash(new_password, method='scrypt', salt_length=16)

        # Update the user's password
        user.password = hashed_new_password
        db.session.commit()

        return True