from flask import Blueprint, request, jsonify
from app.controllers.public_controllers import sign_up_controller, sign_in_controller, show_basic_user_controller, index_users_controller, index_products_controller, show_product_controller

public_blueprint = Blueprint("public", __name__, url_prefix="/api/public")

@public_blueprint.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# ----- Users

@public_blueprint.route('/sign-up', methods=['POST'])
def sign_up_route():
    data = request.get_json()
    token = sign_up_controller(data)
    return jsonify({"token": token}), 201

@public_blueprint.route('/sign-in', methods=['POST'])
def sign_in_route():
    data = request.get_json()
    token = sign_in_controller(data)
    return jsonify({"token": token}), 201

@public_blueprint.route('/users/<user_username>', methods=['GET'])
def show_user_route(user_username):
    user = show_basic_user_controller(user_username)
    return jsonify({"user": user}), 200

@public_blueprint.route('/users', methods=['GET'])
def index_users_route():
    user_list = index_users_controller()
    return jsonify({"users": user_list}), 200

# ------ Products

@public_blueprint.route('/products', methods=['GET'])
def index_products_route():
    products_list = index_products_controller()
    return jsonify({"products": products_list}), 200

@public_blueprint.route('/products/<product_id>', methods=['GET'])
def show_product_route(product_id):
    product = show_product_controller(product_id)
    return jsonify({"product": product}), 200
