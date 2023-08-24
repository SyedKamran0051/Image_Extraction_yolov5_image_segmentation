from flask import Flask
from controllers.predict_images_controller import predict_images_blueprint
from controllers.login_controller import login_blueprint
from models.user import User
from flask_cors import CORS
from constants import DB_name
from init_db import db

app = Flask(__name__)
CORS(app)
#init db
app.config['SQLALCHEMY_DATABASE_URI'] = DB_name
db.init_app(app)

# Registering blueprints
app.register_blueprint(predict_images_blueprint, url_prefix='/predict_images')

# Registering the login blueprint
app.register_blueprint(login_blueprint, url_prefix='/login')

def init_db():
    with app.app_context():
        db.create_all()


init_db()
# CORS(app, origins=["http://localhost:3000"])
@app.route('/',methods=['GET'])
def index():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True,port=8000)

