from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404
    
    def post(self,name):
        if StoreModel.get_by_name(name):
            return {'message': "store with name '{}' already exists".format(name)},400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return{"message":"An error occured creating this store"}, 500 
        
        return store.json(), 201
    
    def delete(self,name):
        store = StoreModel.get_by_name(name)
        if store:
            store.delete_by_name()
            return {'store':"store with name '{}' removed".format(name)}
        return {'store': "store with name '{}' doesn't exist".format(name)},400
        
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
            