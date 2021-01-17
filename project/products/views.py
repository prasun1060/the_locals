from flask.globals import request
from werkzeug.utils import secure_filename
from project import db, app
from .forms import AddProductForm, EditProductForm, EditProductImageForm
from project.models import BusinessOwner, Product
from flask import Blueprint, redirect, flash, render_template, url_for, request, send_from_directory
from flask_login import login_required, current_user
import os

products_blueprint = Blueprint(name='product', import_name=__name__, template_folder='templates/products', static_folder='static')

@products_blueprint.route('/')
def all_products():

    products = Product.query.all()

    return [product.get_json() for product in products]

@products_blueprint.route('/groceries')
def all_groceries():

    products = Product.query.filter_by(product_type='Grocery').all()
    output = list()
    for product in products:

        output.append({
            'id': product.id,
            'product_name': product.product_name,
            'product_image': product.product_image,
            'product_description': product.product_description,
            'product_type': product.product_type,
            'product_quantity': product.product_quantity,
            'product_quantity_units': product.product_quantity_units,
            'mrp': product.mrp,
            'discount': product.discount,
            'price': product.price,
            'rating': product.rating,
            'business_owner_id': product.business_owner_id,
            'business_owner_name': product.business_owner.business_name,
            'availibility_in_no': product.availibility_in_no
        })

    return render_template('grocery.html', products=output)

@products_blueprint.route('/pharmacy_products')
def all_pharmacies():

    products = Product.query.filter_by(product_type='Pharmacy').all()

    return render_template('pharmacy.html', products=products)

@products_blueprint.route('/my_products')
@login_required
def my_products():

    business_owner_id = BusinessOwner.query.filter_by(phone_number=current_user.phone_number).first().id
    products = Product.query.filter_by(business_owner_id=business_owner_id).all()

    return render_template('my_product.html', products=products)

@products_blueprint.route('/add_product', methods=['POST', 'GET'])
@login_required
def add_product():

    if current_user.user_role == 'Customer':

        return redirect(url_for('index'))

    form = AddProductForm()

    if form.validate_on_submit():
        product_image = request.files[form.product_image.name]
        image_ext = product_image.filename.split('.')[-1]
        business_owner = BusinessOwner.query.filter_by(phone_number=current_user.phone_number).first()
        image_name = str(current_user.phone_number) + str(len(Product.query.filter_by(business_owner_id=business_owner.id).all())) + form.product_name.data.replace('/', '') + "." + image_ext
        product = Product(product_name=form.product_name.data,
                            product_image=image_name,
                            product_type=form.product_type.data,
                            product_description=form.product_description.data,
                            product_quantity=form.product_quantity.data,
                            product_quantity_units=form.product_quantity_units.data,
                            mrp=form.mrp.data,
                            discount=form.discount.data,
                            price=form.price.data,
                            business_owner_id=business_owner.id,
                            availibility_in_no=form.availibility_in_no.data)

        db.session.add(product)
        db.session.commit()
        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'product_image/' + image_name))

        flash('Product successfully added!', 'success')

        return redirect(url_for('product.add_product'))
    
    return render_template('add_product.html', form=form)

@products_blueprint.route('/view_product/<int:id>')
def view_product(id):

    product = Product.query.get(id)
    return render_template('view_product.html', product=product)

@products_blueprint.route('/delete/<int:id>')
@login_required
def delete_product(id):

    product = Product.query.get(id)
    product_type = product.product_type
    db.session.delete(product)
    db.session.commit()

    if product_type == 'Grocery':
        return redirect(url_for('product.all_groceries'))
    else:
        return redirect(url_for('product.all_pharmacies'))

@products_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):

    product = Product.query.get(id)

    form = EditProductForm()

    if form.validate_on_submit():

        product = Product.query.get(id)

        product.product_name = form.product_name.data
        product.product_type = form.product_type.data
        product.product_description = form.product_description.data
        product.product_quantity = form.product_quantity.data 
        product.product_quantity_units = form.product_quantity_units.data
        product.mrp = form.mrp.data
        product.discount = form.discount.data
        product.price = form.price.data
        product.availibility_in_no = form.availibility_in_no.data

        db.session.commit()

        flash('Product successfully edited', 'success')

        return redirect(url_for('product.edit_product', id=product.id))

    form.product_name.data = product.product_name
    form.product_type.data = product.product_type
    form.product_description.data = product.product_description
    form.product_quantity.data = product.product_quantity
    form.product_quantity_units.data = product.product_quantity_units
    form.mrp.data = product.mrp
    form.discount.data = product.discount
    form.price.data = product.price
    form.availibility_in_no.data = product.availibility_in_no

    return render_template('edit_product.html', form=form, product=product)

@products_blueprint.route('/edit/edit_image/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product_image(id):

    form = EditProductImageForm()

    if form.validate_on_submit():

        product = Product.query.get(id)
        product_image = request.files[form.product_image.name]
        image_ext = product_image.filename.split('.')[-1]
        image_name = product.product_image.split('.')[0] + '.' + image_ext
        product.product_image = image_name
        db.session.commit()
        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'product_image/' + image_name))

    return render_template('edit_product_image.html', form=form)

@products_blueprint.route('/uploads/product_image/<string:image_name>')
def get_product_image(image_name:str):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'] + '\\product_image',
                               image_name)