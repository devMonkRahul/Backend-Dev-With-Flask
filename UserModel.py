from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, db):
        self.collection = db['User']

    def add_user(self, name, email):
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        data = dict()
        data['name'] = self.name
        data['email'] = self.email
        data['password'] = self.password
        existed_user = self.collection.find_one({"email": self.email})
        if existed_user:
            return False
        self.collection.insert_one(data)
        return True

    def get_user(self):
        return list(self.collection.find())
    
    def get_user_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)}, {"password": 0})
    
    def get_user_by_email(self, email):
        data = self.collection.find_one({"email": email})
        if data: 
            self.name = data['name']
            self.email = data['email']
            self.password = data['password']
            return data
        else:
            return None