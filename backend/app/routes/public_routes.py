from flask import Blueprint

public_blueprint = Blueprint("public", __name__)

@public_blueprint.route("/")
def hello_world():
    return "<p>Hello, World!</p>"