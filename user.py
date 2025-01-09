from flask import Blueprint, request, jsonify
from UserModel import User
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)

db = None

@user_bp.record
def load_db(state):
    global db
    db = state.options['db']

def format_data(data):
    data["_id"] = str(data["_id"])
    if "password" in data:
        del data["password"]
    return data 

@user_bp.get('/getUser')
@jwt_required()
def get_user():
    user = User(db)
    data = user.get_user()
    if (len(data) == 0):
        return jsonify({
            'message': 'No data found!',
        }), 204
    return jsonify({"users": [format_data(item) for item in data]}), 200