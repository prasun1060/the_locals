from flask.globals import request
from flask.helpers import url_for
from project import app, db
from project.models import Customer, Order, Product, BusinessOwner
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

orders_blueprint = Blueprint('orders', __name__, template_folder='templates/orders')

@orders_blueprint.route('/add_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():

    if request.method == 'POST':
        order_quantity = request.form['order_quantity']
        product_id = request.form['product_id']
        if current_user.user_role == 'Customer':
            customer_id=Customer.query.filter_by(phone_number=current_user.phone_number).first().id
        else:
            customer_id=BusinessOwner.query.filter_by(phone_number=current_user.phone_number).first().id
        order = Order(customer_id=customer_id,
                        product_id=product_id,
                        order_quantity=order_quantity,
                        bucket_type='Cart')
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('product.view_product', id=product_id))

    return redirect(url_for('index'))

@orders_blueprint.route('/cart')
@login_required
def view_cart():

    customer = Customer.query.filter_by(phone_number=current_user.phone_number).first()
    cart_products = customer.orders.filter_by(bucket_type='Cart')

    return render_template('cart.html', orders=cart_products)

@orders_blueprint.route('/delete/<int:order_id>')
@login_required
def delete_order(order_id:int):

    order = Order.query.get(order_id)

    db.session.delete(order)
    db.session.commit()

    return redirect(request.referrer)