from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, SubmitField, FloatField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired

class AddProductForm(FlaskForm):

    product_name = StringField(label='Product Name: ', validators=[InputRequired()])
    product_image = FileField(label='Product Image: ', validators=[InputRequired()])
    product_type = SelectField(label='Product Type: ', choices=[('Grocery', 'Grocery'), ('Pharmacy', 'Pharmacy')], validators=[InputRequired()])
    product_description = TextAreaField(label='Product Description: ', validators=[InputRequired()])
    product_quantity = FloatField(label='Product Quantity: ', validators=[InputRequired()])
    product_quantity_units = SelectField(label='Product Quantity Units: ', 
                                            choices=[
                                                ('kg', 'kg'),
                                                ('gm', 'gm'),
                                                ('ft', 'ft'),
                                                ('m', 'm'),
                                                ('ml', 'ml'),
                                                ('litre', 'litre'),
                                                ('pc', 'pc'),
                                                ('packet', 'packet'),
                                                ('unit', 'unit')
                                            ],
                                            validators=[InputRequired()])
    mrp = FloatField(label='MRP: ', validators=[InputRequired()])
    discount = FloatField(label='Discount: ', validators=[InputRequired()])
    price = FloatField(label='Price: ', validators=[InputRequired()])
    availibility_in_no = FloatField(label='Availibilty in No.: ', validators=[InputRequired()])
    submit_btn = SubmitField(label='Add Product')

class EditProductForm(FlaskForm):

    product_name = StringField(label='Product Name: ', validators=[InputRequired()])
    product_type = SelectField(label='Product Type: ', choices=[('Grocery', 'Grocery'), ('Pharmacy', 'Pharmacy')], validators=[InputRequired()])
    product_description = TextAreaField(label='Product Description: ', validators=[InputRequired()])
    product_quantity = FloatField(label='Product Quantity: ', validators=[InputRequired()])
    product_quantity_units = SelectField(label='Product Quantity Units: ', 
                                            choices=[
                                                ('kg', 'kg'),
                                                ('gm', 'gm'),
                                                ('ft', 'ft'),
                                                ('m', 'm'),
                                                ('ml', 'ml'),
                                                ('litre', 'litre'),
                                                ('pc', 'pc'),
                                                ('packet', 'packet'),
                                                ('unit', 'unit')
                                            ],
                                            validators=[InputRequired()])
    mrp = FloatField(label='MRP: ', validators=[InputRequired()])
    discount = FloatField(label='Discount: ', validators=[InputRequired()])
    price = FloatField(label='Price: ', validators=[InputRequired()])
    availibility_in_no = FloatField(label='Availibilty in No.: ', validators=[InputRequired()])
    submit_btn = SubmitField(label='Edit Product')

class EditProductImageForm(FlaskForm):

    product_image = FileField(label='Product Image: ', validators=[InputRequired()])
    submit_btn = SubmitField(label='Edit Image')