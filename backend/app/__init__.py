from flask import Flask
from app.routes.public_routes import public_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(public_blueprint)
    return app

# to use FAST API


