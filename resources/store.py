from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('location', required=True, type=str, help='required')

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.get_json()
        return {'message':'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        # look if store is present
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'message': f'store {name} already present '}, 400
        
        message = Store.parser.parse_args()
        new_store = StoreModel(name, message['location'])

        new_store.save_to_db()
        return new_store.get_json(), 201

    @jwt_required()
    def put(self, name):
        message = Store.parser.parse_args()
        store = StoreModel.find_store_by_name(name)

        if store:
            #update
            store.location = message['location']
        else:
            #create
            store = StoreModel(name, message['location'])
        
        store.save_to_db()
        return store.get_json()

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted'}
        
        return {'message': 'store not found'}, 404

class StoreList(Resource):
    @jwt_required()
    def get(self):
        
        stores = [store.get_json() for store in StoreModel.query.all()]
        return {'stores':stores}
