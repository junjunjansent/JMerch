from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)
    
    # ----- routes
    from app.routes.public_routes import public_blueprint
    app.register_blueprint(public_blueprint)

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


