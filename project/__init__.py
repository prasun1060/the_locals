import os
from flask import Flask, render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

from .models import *

login_manager.init_app(app)
login_manager.login_view = 'login'

from project.api.api import CartCountAPI, UserDetails, identity, authenticate, AllProductAPI
from flask_jwt import JWT

api = Api(app)
jwt = JWT(app, authenticate, identity)
api.add_resource(UserDetails, '/api/user_details/<int:phone_number>')
api.add_resource(AllProductAPI, '/api/all_products')
api.add_resource(CartCountAPI, '/api/cart_count/<int:phone_number>')

from project.business_owners.views import business_blueprint
from project.products.views import products_blueprint
from project.orders.views import orders_blueprint
from project.search.views import search_blueprint

app.register_blueprint(business_blueprint, url_prefix='/business_owners')
app.register_blueprint(products_blueprint, url_prefix='/products')
app.register_blueprint(orders_blueprint, url_prefix='/orders')
app.register_blueprint(search_blueprint, url_prefix='/search')