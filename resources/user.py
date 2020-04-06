import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='this is required')
    parser.add_argument('password', type=str, required=True, help='this is required')
      

    def post(self):
        #Parse data using the defined parser
        data = UserRegister.parser.parse_args()

        #check if user already present
        if UserModel.find_by_username(data['username']):
            return {'message':'user already registerd!'}

        new_user = UserModel(data['username'], data['password'])
        new_user.save_to_db()

        return {"message": "User created successfuly"}, 201