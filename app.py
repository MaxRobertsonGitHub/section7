import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.items import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from db import db

uri = os.getenv("DATABASE_URL",'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# flask restful takes care of jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'blah'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store,'/store/<string:name>') 
api.add_resource(StoreList,'/stores')    
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)

