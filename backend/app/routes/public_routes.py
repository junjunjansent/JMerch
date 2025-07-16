from flask import Blueprint, request, jsonify
from app.controllers.public_controllers import sign_up_controller, sign_in_controller, show_user_controller, index_users_controller

public_blueprint = Blueprint("public", __name__, url_prefix="/api/public")

@public_blueprint.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

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

@public_blueprint.route('/users/<userUsername>', methods=['GET'])
def show_user_route(userUsername):
    user = show_user_controller(userUsername)
    return jsonify({"user": user}), 200

@public_blueprint.route('/users', methods=['GET'])
def index_users_route():
    user_list = index_users_controller()
    return jsonify({"users": user_list}), 200
