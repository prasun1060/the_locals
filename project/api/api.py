from project.models import Order, User, Customer, BusinessOwner, Product
from project import db
from flask_restful import Resource, Api
from werkzeug import check_password_hash
from flask_jwt import jwt_required

def authenticate(username, password):

    user = User.query.filter_by(phone_number=username).first()

    if user is not None and user.password==password:

        return user

def identity(payload):

    user_id = payload['identity']

    return User.query.get(user_id)

class CartCountAPI(Resource):

    @jwt_required()
    def get(self, phone_number):
        customer = Customer.query.filter_by(phone_number=phone_number).first()
        print(len(customer.orders.all()))
        return {
            'cart_count': len(customer.orders.filter_by(bucket_type='Cart').all())
        }

class UserDetails(Resource):

    @jwt_required()
    def get(self, phone_number):

        user = User.query.filter_by(phone_number=phone_number).first()

        if user.user_role == 'Customer':

            customer = Customer.query.filter_by(phone_number=phone_number).first()

            return {
                'data_found': True,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'address1': customer.address1,
                'address2': customer.address2,
                'city': customer.city,
                'zip': customer.zip,
                'state': customer.state,
                'country': customer.country,
                'phone_number': customer.phone_number,
                'email': customer.email,
                'sex': customer.sex,
                'date_of_birth': customer.date_of_birth.strftime('%d-%m-%Y')
            }
        
        elif user.user_role == 'Business':

            business_owner = BusinessOwner.query.filter_by(phone_number=phone_number).first()

            return {
                'data_found': True,
                'business_name': business_owner.business_name,
                'address1': business_owner.address1,
                'address2': business_owner.address2,
                'city': business_owner.city,
                'zip': business_owner.zip,
                'state': business_owner.state,
                'country': business_owner.country,
                'phone_number': business_owner.phone_number,
                'business_category': business_owner.business_category
            }
        
        else:

            return {
                'data_found': False
            }, 404

class ProductAPI(Resource):

    def get(self, id):

        product = Product.query.get(id)
        return product.get_json()
    
    @jwt_required()
    def delete(self, id):

        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()

        return {"message": "success"}

    @jwt_required()
    def post(self, 
                product_name, product_image,
                product_description, product_quantity, product_quantity_units,
                price, rating,
                business_owner_id, availibity_in_no):
        
        product = Product(product_name, product_image,
                            product_description, product_quantity, product_quantity_units,
                            price, rating,
                            business_owner_id, availibity_in_no)
        
        db.session.add(product)
        db.session.commit()

        return {"message": "success"}

class AllProductAPI(Resource):

    def get(self):

        products = Product.query.all()

        return [product.get_json() for product in products]