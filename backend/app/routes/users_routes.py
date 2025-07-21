from flask import Blueprint, request, jsonify, g
from app.controllers.users_controllers import show_full_user_controller, update_owner_controller, update_owner_password_controller
from app.middlewares.auth_middleware import token_required

users_blueprint = Blueprint("users", __name__, url_prefix="/api/users")

@users_blueprint.route("/owner", methods=['GET'])
@token_required
def show_owner_route():
    user_id = str(g.user['id'])
    user = show_full_user_controller(user_id)
    return jsonify({"user": user}), 200

@users_blueprint.route("/owner", methods=['PUT'])
@token_required
def update_owner():
    data = request.get_json()
    user_id = str(g.user['id'])
    # will return an updated token
    updated_user, token = update_owner_controller(data, user_id)
    return jsonify({"user": updated_user, "token": token}), 201

@users_blueprint.route("/owner/password", methods=['PUT'])
@token_required
def update_owner_password():
    data = request.get_json()
    user_id = str(g.user['id'])
    updated_user = update_owner_password_controller(data, user_id)
    return jsonify({"user": updated_user}), 201