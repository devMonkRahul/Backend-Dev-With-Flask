from flask import Blueprint, request, jsonify
from UserModel import User
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

db = None

@auth.record
def load_db(state):
    global db
    db = state.options['db']

@auth.post('/login')
def user_login():
    data = request.json
    user_instance = User(db)
    user = user_instance.get_user_by_email(data['email'])
    if not user:
        return jsonify({
            'message': 'User not found!',
            'status': 400,
        }), 400
    if ('password' in data and user_instance.check_password(data['password'])):
        accessToken = create_access_token(identity=user["email"])
        return jsonify({
            'message': 'Login successful!',
            'status': 200,
            'accessToken': accessToken,
        }), 200
    return jsonify({
        'message': 'Invalid credentials!',
        'status': 401,
    }), 401