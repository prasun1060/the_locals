from project import app, models
from project.models import BusinessOwner
from flask import Blueprint, request, render_template, send_from_directory

business_blueprint = Blueprint('business', __name__, template_folder='templates/business_owners')

@business_blueprint.route('/')
def stores():

    stores = BusinessOwner.query.all()

    data = [store.get_json() for store in stores]

    return render_template('stores.html', stores=data)

@business_blueprint.route('/uploads/business_logo/<string:logoname>')
def get_business_logo(logoname:str):
    
    return send_from_directory(app.config['UPLOAD_FOLDER'] + '\\business_logo',
                               logoname)