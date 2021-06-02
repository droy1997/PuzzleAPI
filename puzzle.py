from pymongo import MongoClient
from bson import json_util
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import enum

class Database():
    url = "mongodb://localhost:5000/"
    database = "GameTest"
    collection = "puzzles"


class Difficulty(enum.Enum): 
    veryeasy = 1
    easy = 2
    medium = 3
    difficult = 4
    verydifficult = 5


class Puzzle(Resource):
    
    @staticmethod
    def fetch_and_validate_data():
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=False, help="This field cannot be left blank!")
        parser.add_argument('agegroup', type=str, required=False, help="This field cannot be left blank!")
        parser.add_argument('difficulty', type=str, required=False, help="This field cannot be left blank!")
        return parser.parse_args()
        
    
    def post(self, number="1"):
        request_data = Puzzle.fetch_and_validate_data()
        query = {k: v for k, v in request_data.items() if v is not None}
        client = MongoClient(Database.url)
        database = Database.database
        collection = Database.collection
        cursor = client[database]
        collection = cursor[collection]
        documents = collection.find(query)
        response = [{item: data1[item] for item in data1 if item != '_id'} for data1 in documents]
        client.close()
        return {'puzzles': str(response)}, 200

class PuzzleCreate(Resource):
    
    @staticmethod
    def fetch_and_validate_data():
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('agegroup', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('difficulty', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('question', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('answer', type=dict, required=True, help="This field cannot be left blank!")
        parser.add_argument('meta', type=dict, required=False, help="This field cannot be left blank!")
        data = parser.parse_args()
        answer_parser = reqparse.RequestParser()
        answer_parser.add_argument('type', type=str, required=True, location=('answer',))
        answer_parser.add_argument('value', type=list, required=True, location=('answer',))
        return data
    
    # @jwt_required()
    def post(self):
        data = PuzzleCreate.fetch_and_validate_data() 
        client = MongoClient(Database.url)
        database = Database.database
        collection = Database.collection
        cursor = client[database]
        collection = cursor[collection]
        response = collection.insert_one(data)
        client.close()
        return {'Status': 'Puzzle created.', 'Document_ID': str(response.inserted_id)}, 201

class PuzzleUpdate(Resource):
    
    @staticmethod
    def fetch_and_validate_data():
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('agegroup', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('difficulty', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('question', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('answer', type=dict, required=True, help="This field cannot be left blank!")
        parser.add_argument('meta', type=dict, required=False, help="This field cannot be left blank!")
        data = parser.parse_args()
        answer_parser = reqparse.RequestParser()
        answer_parser.add_argument('type', type=str, required=True, location=('answer',))
        answer_parser.add_argument('value', type=list, required=True, location=('answer',))
        return data
    
    # @jwt_required()
    def post(self):
        data = PuzzleCreate.fetch_and_validate_data() 
        client = MongoClient(Database.url)
        database = Database.database
        collection = Database.collection
        cursor = client[database]
        collection = cursor[collection]
        response = collection.insert_one(data)
        client.close()
        return {'Status': 'Puzzle updated.', 'Document_ID': str(response.inserted_id)}, 201
