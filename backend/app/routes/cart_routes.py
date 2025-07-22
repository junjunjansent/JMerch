from flask import Blueprint, request, jsonify, g
from app.controllers.cart_controllers import show_cart_controller, create_cart_controller, update_cart_controller, destroy_cart_controller
from app.middlewares.auth_middleware import token_required

cart_blueprint = Blueprint("cart", __name__, url_prefix="/api/cart")

@cart_blueprint.route("/", methods=['GET'])
@token_required
def show_cart_route():
    user_id = str(g.user['id'])
    cart = show_cart_controller(user_id)
    return jsonify({"cart": cart}), 200

@cart_blueprint.route("/", methods=['POST'])
@token_required
def create_cart_route():
    user_id = str(g.user['id'])
    data = request.get_json()
    cart = create_cart_controller(data, user_id)
    return jsonify({"cart": cart}), 201

@cart_blueprint.route("/", methods=['PUT'])
@token_required
def update_cart_route():
    user_id = str(g.user['id'])
    data = request.get_json()
    cart = update_cart_controller(data, user_id)
    return jsonify({"cart": cart}), 201

@cart_blueprint.route("/", methods=['DELETE'])
@token_required
def destroy_cart_route():
    user_id = str(g.user['id'])
    cart = destroy_cart_controller(user_id)
    return jsonify({"cart": cart}), 200