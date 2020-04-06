from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

"""
Error codes
200: ok
201: created
202: delayed
400: bad request (already exists)
404: not found
500: internal server error
"""

class Item(Resource):
    # used to get the required argument only and neglect the rest
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this is required')
    parser.add_argument('store_id', type=int, required=True, help='this is required')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.get_json()
        else:
            return {'message':'item not found'}, 404

    @jwt_required()
    def post(self, name):
        #look if item already exists
        row = ItemModel.find_by_name(name)
        if row:
            return {'Message': f'item with name {name} already exists'}, 400
        
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'Error occured inserting into DB'}, 500

        return item.get_json(), 201

    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()

        found_item = ItemModel.find_by_name(name)
        new_item = ItemModel(name, request_data['price'], request_data['store_id'])

        if found_item is None:
            new_item.save_to_db()
            return new_item.get_json(), 201
        else:
            found_item.price = request_data['price']
            found_item.store_id = request_data['store_id']
            found_item.save_to_db()
            return found_item.get_json(), 201
        
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return item.get_json()
        return {'message': 'item not found'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        
        items = [item.get_json() for item in ItemModel.query.all()]
        return {'items':items}
