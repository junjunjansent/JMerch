from flask import Flask, jsonify, request
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, supports_credentials=True, expose_headers=["Authorization"])
    # TODO - may need to fix
    # CORS(app, supports_credentials=True,
    #  origins=["http://localhost:5173"],
    #  allow_headers=["Content-Type", "Authorization"],
    #  expose_headers=["Authorization"],
    #  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # ----- routes
    from app.routes.public_routes import public_blueprint
    app.register_blueprint(public_blueprint)

    # # Express (with middleware like cors) handles preflight (OPTIONS) requests
    # #  for you automatically — whereas in Flask, you often have to explicitly configure or allow it.
    # @app.before_request
    # def skip_auth_for_options():
    #     if request.method == 'OPTIONS':
    #         print("hit something on global")
    #         return '', 200

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




