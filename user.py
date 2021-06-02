from pymongo import MongoClient
from bson import json_util
from flask import Flask, request, json, Response
from flask_restful import Resource, reqparse

class Database():
    url = "mongodb://localhost:5000/"
    database = "GameTest"
    collection = "users"

def parse_json(data):
    return json.loads(json_util.dumps(data))

class User(object):
    
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __str__(self):
        return ("id: "+self.id +" username: "+self.username)
    
    @classmethod
    def find_by_username(cls, username):
        client = MongoClient(Database.url)
        database = Database.database
        collection = Database.collection
        cursor = client[database]
        collection = cursor[collection]
        doc = collection.find_one({"username": username})
        doc = parse_json(doc)
        if doc:
            user = cls(str(doc["_id"]["$oid"]),doc["username"],doc["password"])
        else:
            user = None
        client.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        client = MongoClient("mongodb://localhost:5000/")
        database = "GameTest"
        collection = "users"
        cursor = client[database]
        collection = cursor[collection]
        doc = collection.find_one({"_id": _id})
        if doc:
            user = cls(doc["_id"],doc["username"],doc["password"])
        else:
            user = None
        client.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required = True, help="This Field cannot be blank.") 
    parser.add_argument("password", type=str, required = True, help="This Field cannot be blank.") 
    
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data["username"]):
            return {"message": "A user with that user name already exists" }, 400
        client = MongoClient(Database.url)
        database = Database.database
        collection = Database.collection
        cursor = client[database]
        collection = cursor[collection]
        response = collection.insert_one(data)
        client.close()
        output = {'Status': 'User created.',
                  'Document_ID': str(response.inserted_id)}
        return output, 201





# if __name__ == '__main__':
#     user = User.find_by_username("demouser")
#     print(user)
