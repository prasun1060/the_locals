from flask.globals import current_app
from project import app, db
from project.models import BusinessOwner, Customer, User
from project.forms import CustomerRegistrationForm, LoginForm, RegistrationForm, BusinessOwnerRegistrationForm
from flask import render_template, request, redirect, flash, url_for, session, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
import os

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(phone_number=login_form.phone_number.data).first()

        if user is not None:

            if user.check_password(login_form.password.data):

                login_user(user=user)
                flash('Logged in successfully!', 'success')

                next_page = request.args.get('next')
                
                if user.user_role == 'Customer' and Customer.query.filter_by(phone_number=user.phone_number).first() is None:
                    
                    next_page = url_for('customer_registration')
                
                elif user.user_role == 'Business' and BusinessOwner.query.filter_by(phone_number=user.phone_number).first() is None:
                    
                    next_page = url_for('business_registration')

                if next_page is None or next_page == '/':

                    next_page = url_for('index')
                
                return redirect(next_page)
            
            else:

                flash('Please check your password and try again.', 'warning')
                return redirect(url_for('login'))
        
        else:

            flash('Please check your phone number and try again.', 'warning')
            return redirect(url_for('login'))

    return render_template('login.html', form=login_form)

@app.route('/logout')
@login_required
def logout():

    logout_user()
    session.pop('user_details', None)
    flash('You are successfully logged out', 'success')
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST', 'GET'])
def register_user():

    form = RegistrationForm()

    if form.validate_on_submit():

        if User.query.filter_by(phone_number=form.phone_number.data).first() is not None:

            flash(f'Account alreay present with phone number {form.phone_number.data}. Try again with a different one.', 'warning')
            return redirect(url_for('register_user'))

        user = User(user_role=form.user_role.data,
                        phone_number=form.phone_number.data,
                        password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Thanks for registering with us.', 'success')

        if form.user_role.data == 'Customer':

            return redirect(url_for('customer_registration'))
        
        else:

            return redirect(url_for('business_registration'))
        # if form.check_phone_number(field=form.phone_number.data):
        #     pass
    
    return render_template('register_user.html', form=form)

@app.route('/customer_signup', methods=['POST', 'GET'])
@login_required
def customer_registration():

    form = CustomerRegistrationForm()

    if form.validate_on_submit():
        print('validated')
        user = Customer(first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            address1=form.address1.data,
                            address2=form.address2.data,
                            city=form.city.data,
                            zip=form.zip.data,
                            state=form.state.data,
                            country=form.country.data,
                            phone_number=form.phone_number.data,
                            email=form.email.data,
                            sex=form.sex.data,
                            date_of_birth=form.date_of_birth.data)
        db.session.add(user)
        db.session.commit()

        flash('You are now successfully registered as customer.', 'success')

        next_page = request.args.get('next')

        if next_page is None:

            next_page = url_for('index')

        return redirect(next_page)
    return render_template('customer_registration.html', form=form)

@app.route('/business_signup', methods=['POST', 'GET'])
@login_required
def business_registration():

    form = BusinessOwnerRegistrationForm()

    if form.validate_on_submit():
        business_logo = request.files[form.business_logo.name]
        business_logo_ext = business_logo.filename.split('.')[-1]
        business_logo_name = str(current_user.phone_number) + '.' + business_logo_ext
        user = BusinessOwner(business_name=form.business_name.data,
                            business_logo=business_logo_name,
                            address1=form.address1.data,
                            address2=form.address2.data,
                            city=form.city.data,
                            zip=form.zip.data,
                            state=form.state.data,
                            country=form.country.data,
                            phone_number=current_user.phone_number,
                            business_category=form.business_category.data)
        db.session.add(user)
        db.session.commit()

        business_logo.save(os.path.join(app.config['UPLOAD_FOLDER'], 'business_logo\\' + business_logo_name))

        flash('You are now successfully registered as business.', 'success')

        next_page = request.args.get('next')

        if next_page is None:

            next_page = url_for('index')

        return redirect(next_page)
    
    return render_template('business_registration.html', form=form)

@app.route('/uploads/<string:filename>')
def uploaded_file(filename:str):

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
                        
if __name__ == "__main__":

    app.run(host='0.0.0.0', port=80, debug=True)