from flask import Flask, request, jsonify
from dbConfig import connect_db
from UserModel import User
from auth import auth
from jwtConfig import jwt_config
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db = connect_db(app)
jwt_config(app)

app.register_blueprint(auth, url_prefix='/auth', db=db)

@app.route('/')
def home():
    return jsonify({
        "message": "Python Server is Running!",
        "status": 200,
    })

@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.json
    user = User(db)
    user.add_user(data['name'], data['email'])
    user.set_password(data['password'])
    status = user.save()
    if not status:
        return jsonify({
            'message': 'User already exists!',
            'status': 409,
        }), 409
    return jsonify({
        'message': 'User added successfully!',
        'user': user.__repr__(),
        "status": 201,
    }), 201

def format_data(data):
    data["_id"] = str(data["_id"])
    if "password" in data:
        del data["password"]
    return data 

@app.route('/getUser', methods=['GET'])
def get_user():
    user = User(db)
    data = user.get_user()
    if (len(data) == 0):
        return jsonify({
            'message': 'No data found!',
        }), 204
    return jsonify([format_data(item) for item in data]), 200

@app.route('/getUserById', methods=['GET'])
def get_user_by_id():
    user = User(db)
    userId = request.args.get('userId')
    data = user.get_user_by_id(userId)
    if data:
        return jsonify(format_data(data)), 200
    else:
        return jsonify({ "message": "Data not found" }), 404

# @app.route('/add', methods=['POST'])
# def add_data():
#     data = request.json  # Get JSON data from the request
#     collection.insert_one(data)  
#     return jsonify({
#         'message': 'Data added successfully!',
#         "status": 201,
#     }), 201

# @app.route('/get', methods=['GET'])
# def get_data():
#     data = list(collection.find())
#     if (len(data) == 0):
#         return jsonify({
#             'message': 'No data found!',
#         }), 204
#     return jsonify([format_data(item) for item in data]), 200

# @app.route('/update', methods=['PUT'])
# def update_data():
#     data = request.json
#     dataId = request.args.get('dataId')

#     if id:
#         result = collection.update_one({"_id": ObjectId(dataId)}, {"$set": data})
#         if result.modified_count:
#             return jsonify({ "message": "Data Updated Successfully" }), 200
#         else:
#             return jsonify({ "message": "Data not found" }), 404
#     else:
#         return jsonify({ "message": "Please provide id" }), 400

if __name__ == '__main__':
    app.run(debug=True, port=4000)