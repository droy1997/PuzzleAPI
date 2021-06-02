from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from puzzle import Puzzle, PuzzleCreate, PuzzleUpdate

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'debasmit'
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(Puzzle, '/puzzle/<string:number>', '/puzzle')
api.add_resource(PuzzleCreate, '/create')
api.add_resource(PuzzleUpdate, '/update')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')  # important to mention debug=True
