import os
from models.user import User
from werkzeug.security import generate_password_hash
from init_db import db  # Replace 'your_database_instance' with the actual module where your SQLAlchemy db instance is initialized

def seed_user():
    # Fetch admin password from environment variable
    admin_password = os.environ.get('ADMIN_PASSWORD', 'default_password')

    # Check if user already exists
    existing_user = User.query.filter_by(username='admin').first()

    if existing_user is None:
        # Hash the password
        hashed_password = generate_password_hash(admin_password, method='sha256')

        # Create a new user
        new_user = User(
            username='admin',
            password=hashed_password
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    else:
        pass  # Admin user already exists

if __name__ == '__main__':
    seed_user()
