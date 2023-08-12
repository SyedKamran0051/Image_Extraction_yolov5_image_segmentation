from flask import Flask
from controllers.predict_images_controller import predict_images_blueprint

app = Flask(__name__)

# Registering blueprints
app.register_blueprint(predict_images_blueprint, url_prefix='/predict_images')

@app.route('/')
def index():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True)

from controllers.login_controller import login_blueprint

# Registering the login blueprint
app.register_blueprint(login_blueprint, url_prefix='/login')
