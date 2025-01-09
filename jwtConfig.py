from flask_jwt_extended import JWTManager

def jwt_config(app):
    jwt = JWTManager()
    jwt.init_app(app)
    return jwt