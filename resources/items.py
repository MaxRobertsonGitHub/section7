from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                            type=float,
                            required=True,
                            help='this field cannot be blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id')
    @jwt_required()
    def get(self,name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'}
    
    def post(self,name):
        if ItemModel.get_by_name(name):
            return {'item': "item with name '{}' already exists".format(name)},400
        data= Item.parser.parse_args()
        
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return{"message":"An error occured inserting the item"}, 500 
        
        return item.json(), 201
    
    def delete(self,name):
        item = ItemModel.get_by_name(name)
        if item:
            item.delete_by_name()
            return {'items':"item with name '{}' removed".format(name)}
        return {'item': "item with name '{}' doesn't exist".format(name)},400
    
    def put(self,name):
        data=Item.parser.parse_args()
        if item is none:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        return item.json()

        
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
            