from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'  # to authenticate and create token 
api = Api(app)

@app.before_first_request
def create_table():
    # create the data.db and all tables (from the items) if not presesnt
    db.create_all()

'''creates a new endpoint /auth
receives a dict {'username':'u', 'password':'p'} 
in the POST header request to /auth
returns a token'''
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:6060/item/chair
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    # run app if this file is main
    db.init_app(app)
    app.run(port=6060, debug=True)