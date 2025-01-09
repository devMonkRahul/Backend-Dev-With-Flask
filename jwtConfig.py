from flask_jwt_extended import JWTManager

def jwt_config(app):
    JWTManager().init_app(app)