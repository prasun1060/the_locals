from enum import unique
from sqlalchemy.orm import backref
from project import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):

    user =  User.query.get(user_id)

    return user

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_role = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, user_role:str, phone_number:int, password:str) -> None:

        self.user_role = user_role
        self.phone_number = phone_number
        self.password = generate_password_hash(password=password)

    def check_password(self, password:str) -> bool:

        return check_password_hash(self.password, password)

class Customer(db.Model):

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    profile_pic = db.Column(db.Text, nullable=True)
    address1 = db.Column(db.Text, nullable=False)
    address2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    sex = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def __init__(self, 
                    first_name, last_name, 
                    address1, address2, city, zip, state, country,
                    phone_number, email, sex, date_of_birth) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.zip = zip
        self.state = state
        self.country = country
        self.phone_number = phone_number
        self.email = email
        self.sex = sex
        self.date_of_birth = date_of_birth
    
    # def get_order_ids(self):

    #     output = list
        
    #     for order in self.orders:

    #         output['']
            
class BusinessOwner(db.Model):

    __tablename__ = 'business_owners'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    business_name = db.Column(db.Text, nullable=False)
    business_logo = db.Column(db.Text, nullable=True)
    address1 = db.Column(db.Text, nullable=False)
    address2 = db.Column(db.Text)
    city = db.Column(db.Text, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    business_category = db.Column(db.Text, nullable=True, unique=False)
    products = db.relationship('Product', backref='business_owner', lazy='dynamic')

    def __init__(self, 
                    business_name, business_logo, 
                    address1, address2, city, zip, state, country,
                    phone_number, business_category) -> None:

        self.business_name = business_name
        self.business_logo = business_logo
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.zip = zip
        self.state = state
        self.country = country
        self.phone_number = phone_number
        self.business_category = business_category

    def get_json(self):

        return {
            "id": self.id,
            "business_name": self.business_name,
            "business_logo": self.business_logo,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "zip": self.zip,
            "state": self.state,
            "country": self.country,
            "phone_number": self.phone_number,
            "business_category": self.business_category
        }

class Product(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_name = db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text, nullable=False)
    product_description = db.Column(db.Text, nullable=False)
    product_type = db.Column(db.Text, nullable=False)
    product_quantity = db.Column(db.Float, nullable=False)
    product_quantity_units = db.Column(db.Text, nullable=False)
    mrp = db.Column(db.Float(10), nullable=False)
    discount = db.Column(db.Float(3), nullable=False)
    price = db.Column(db.Float(10), nullable=False)
    rating = db.Column(db.Integer, default=0)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('business_owners.id'), nullable=False)
    availibility_in_no = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='product', lazy='dynamic')

    def __init__(self, 
                    product_name, product_image,
                    product_description, product_type, product_quantity, product_quantity_units,
                    mrp, discount, price,
                    business_owner_id, availibility_in_no) -> None:

        self.product_name = product_name
        self.product_image = product_image
        self.product_description = product_description
        self.product_type = product_type
        self.product_quantity = product_quantity
        self.product_quantity_units = product_quantity_units
        self.mrp = mrp
        self.discount = discount
        self.price = price
        self.business_owner_id = business_owner_id
        self.availibility_in_no = availibility_in_no

    def get_json(self):

        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_image': self.product_image,
            'product_description': self.product_description,
            'product_type': self.product_type,
            'product_quantity': self.product_quantity,
            'product_quantity_units': self.product_quantity_units,
            'mrp': self.mrp,
            'discount': self.discount,
            'price': self.price,
            'rating': self.rating,
            'business_owner_id': self.business_owner_id,
            'availibility_in_no': self.availibility_in_no
        }

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False)
    bucket_type = db.Column(db.String, nullable=False)

    def __init__(self, customer_id:int, product_id:int, order_quantity:int, bucket_type:str) -> None:

        self.customer_id = customer_id
        self.product_id =product_id
        self.order_quantity = order_quantity
        self.bucket_type = bucket_type