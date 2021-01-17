from types import MethodDescriptorType
from project.models import Product, BusinessOwner
from project import app, db
from flask import Blueprint, render_template, request, redirect, url_for

search_blueprint = Blueprint('search', __name__, template_folder='templates/search')

@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'GET':
        query = request.args.get('query')
        
        products = Product.query.filter(Product.product_name.like('%' + query +  '%')).all()
        stores = BusinessOwner.query.filter(BusinessOwner.business_name.like('%' + query +  '%')).all()
        return render_template('search.html', products=products, stores=stores)
    
    return redirect(url_for('index'))