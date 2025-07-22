from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # ----- routes
    from app.routes.public_routes import public_blueprint
    app.register_blueprint(public_blueprint)

    from app.routes.users_routes import users_blueprint
    from app.routes.cart_routes import cart_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(cart_blueprint)

    # ----- error Handler
    from app.utils.error_handler import APIError

    @app.errorhandler(APIError)
    def api_error_handler(error):
        return jsonify({
            "error": [{
                "status": error.status,
                "source": {"pointer": error.pointer},
                "title": error.title,
                "detail": error.detail
            }]}), error.status

    return app




