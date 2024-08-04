from flask import Flask
from flask_cors import CORS
from db import db
from flask_migrate import Migrate
from routes.rol_router import rol_router 
from routes.user_router import user_router
from routes.category_router import category_router
from routes.product_router import product_router
from routes.order_router import order_router
from flask_jwt_extended import JWTManager
from config import Config

from models import (
   category_model,
   product_model,
   order_detail_model,
   order_model,
   rol_model,
   user_model,
   updated_product_logs,
)

app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
# app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
cors = CORS(app)

app.register_blueprint(rol_router, url_prefix='/api/rol')
app.register_blueprint(user_router, url_prefix='/api/user')
app.register_blueprint(category_router, url_prefix='/api/category')
app.register_blueprint(product_router, url_prefix='/api/product')
app.register_blueprint(order_router, url_prefix='/api/order')

if __name__ == '__main__':
   app.run(debug=True)


