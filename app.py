from flask import Flask, request, jsonify
from dbConfig import connect_db
from UserModel import User
from auth import auth
from user import user_bp
from jwtConfig import jwt_config
# from jwtConfig import jwt
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db = connect_db(app)
jwt = jwt_config(app)

app.register_blueprint(auth, url_prefix='/auth', db=db)
app.register_blueprint(user_bp, url_prefix='/user', db=db)

@app.route('/')
def home():
    return jsonify({
        "message": "Python Server is Running!",
        "status": 200,
    })

# @app.route('/addUser', methods=['POST'])
# def add_user():
#     data = request.json
#     user = User(db)
#     user.add_user(data['name'], data['email'])
#     user.set_password(data['password'])
#     status = user.save()
#     if not status:
#         return jsonify({
#             'message': 'User already exists!',
#             'status': 409,
#         }), 409
#     return jsonify({
#         'message': 'User added successfully!',
#         'user': user.__repr__(),
#         "status": 201,
#     }), 201

# def format_data(data):
#     data["_id"] = str(data["_id"])
#     if "password" in data:
#         del data["password"]
#     return data 

# @app.route('/getUser', methods=['GET'])
# def get_user():
#     user = User(db)
#     data = user.get_user()
#     if (len(data) == 0):
#         return jsonify({
#             'message': 'No data found!',
#         }), 204
#     return jsonify([format_data(item) for item in data]), 200

# @app.route('/getUserById', methods=['GET'])
# def get_user_by_id():
#     user = User(db)
#     userId = request.args.get('userId')
#     data = user.get_user_by_id(userId)
#     if data:
#         return jsonify(format_data(data)), 200
#     else:
#         return jsonify({ "message": "Data not found" }), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)