from flask import Flask
import os
from controllers.predict_images_controller import predict_images_blueprint
from controllers.login_controller import login_blueprint
from controllers.dashboard_controller import dashboard_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from seed import seed_user 
from constants import DB_name
from init_db import db

app = Flask(__name__)
CORS(app)
#init db
app.config['SQLALCHEMY_DATABASE_URI'] = DB_name
db.init_app(app)

app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")  # Replace with your own secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Where to look for the JWT tokens

jwt = JWTManager(app)

# Registering blueprints
app.register_blueprint(predict_images_blueprint, url_prefix='/predict_images')

# Registering the login blueprint
app.register_blueprint(login_blueprint, url_prefix='/login')

# Registering the dashboard blueprint
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

def init_db():
    with app.app_context():
        db.create_all()
        seed_user()


init_db()
# CORS(app, origins=["http://localhost:3000"])
@app.route('/',methods=['GET'])
def index():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True,port=8000)

