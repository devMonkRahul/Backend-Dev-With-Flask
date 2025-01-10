from flask_jwt_extended import JWTManager
from flask import jsonify

def jwt_config(app):
    jwt = JWTManager()
    jwt.init_app(app)

    @jwt.expired_token_loader
    def token_expired_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'Token has expired!',
            'status': 401,
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'Invalid token!',
            'status': 401,
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({
            'message': 'Unauthorized!',
            'status': 401,
        }), 401
    
    return jwt