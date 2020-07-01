from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField,\
					 SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, ValidationError, Email, EqualTo
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):

	vendor_name=StringField('Full Name', validators=[ InputRequired(), Length(min=3, max=20)])
	user_name=StringField('User Name', validators=[ InputRequired(), Length(min=3, max=20)])
	vendor_pic=FileField('Vendor pic', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
	email=StringField('Email', validators=[ InputRequired(), Email()])
	address=TextAreaField('Address', validators=[Optional()])
	password=PasswordField('Password',validators=[ InputRequired(), Length(min=3, max=30)])
	confirm_password=PasswordField('Confirm password',validators=[InputRequired(), EqualTo('password')])
	contact=StringField('Tel Number:', validators=[ InputRequired(), Length(min=3, max=20)])
	check=BooleanField('I agree to the Terms and Conditions',  validators=[ InputRequired()])
	submit=SubmitField('Continue to Business Info')

class BusinessForm(FlaskForm):
	tin_number=StringField('TIN Number', validators=[ Optional(), Length(min=3, max=20)])
	shop_name=StringField('Shop Name', validators=[ Optional(), Length(min=3, max=20)])
	company_name=StringField('Company Name', validators=[ Optional(), Length(min=3, max=20)])
	location=TextAreaField('Address', validators=[ InputRequired(), Length(min=3, max=20)])
	description=TextAreaField('Shop/Company Description', validators=[ InputRequired(), Length(min=3, max=20)])
	license_number=StringField('License Number', validators=[ Optional(), Length(min=3, max=20)])
	other_files=FileField('', validators=[FileAllowed(['jpg', 'png'])])
	contact=StringField('Tel Number:', validators=[ InputRequired(), Length(min=3, max=20)])
	submit=SubmitField('Continue to Payment Details')

class LoginForm(FlaskForm):
	email=StringField('Email', validators=[Email(), InputRequired()])
	password=PasswordField('Password',validators=[ InputRequired(), Length(min=3, max=30)])
	submit=SubmitField('Login')

class AddProduct(FlaskForm):
	name=StringField('Name', validators=[ InputRequired(), Length(min=3, max=20)])
	category=SelectField('Category Name', validators=[ InputRequired()], choices=[])
	sub_category=SelectField('Sub_Category Name', validators=[ InputRequired()], choices=[])
	brand=SelectField('Brand', validators=[ InputRequired()], choices=[])
	product_type=StringField('Product Type', validators=[ Optional(), Length(min=3, max=20)])
	size=StringField('Size', validators=[ Optional(), Length(min=3, max=20)])
	color=StringField('Color', validators=[ InputRequired(), Length(min=3, max=20)])
	quantity=StringField('quantity', validators=[ InputRequired(), Length(min=3, max=20)])
	weight=StringField('weight', validators=[ Optional(), Length(min=3, max=20)])
	front_pic=FileField('Front Image', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
	back_pic=FileField('Back Image', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
	description=TextAreaField('Total Product Description', validators=[InputRequired()])
	prize=StringField('Prize', validators=[ Optional(), Length(min=3, max=20)])
	key_features=TextAreaField('Products Key Features', validators=[Optional()])
	warranty=StringField('Warranty', validators=[ Optional(), Length(min=3, max=20)])
	garantee=StringField('Garantee', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Add Product')

class AddStock(FlaskForm):
	price=StringField('Promotional Price', validators=[ Optional(), Length(min=3, max=20)])
	quantity=StringField('Add Quantity', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Submit')

class EditProductForm(FlaskForm):
	name=StringField('Name', validators=[InputRequired(), Length(min=3, max=20)])
	category=SelectField('Category Name', validators=[ InputRequired()], choices=[])
	sub_category=SelectField('Sub_Category Name', validators=[ InputRequired()], choices=[])
	brand=SelectField('Brand', validators=[ InputRequired()], choices=[])
	product_type=StringField('Product Type', validators=[ Optional(), Length(min=3, max=20)])
	size=StringField('Size', validators=[ Optional(), Length(min=3, max=20)])
	color=StringField('Color', validators=[ InputRequired(), Length(min=3, max=20)])
	quantity=StringField('quantity', validators=[ InputRequired(), Length(min=3, max=20)])
	weight=StringField('weight', validators=[ Optional(), Length(min=3, max=20)])
	front_pic=FileField('Front Image', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
	back_pic=FileField('Back Image', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
	description=TextAreaField('Total Product Description', validators=[InputRequired()])
	prize=StringField('Prize', validators=[ Optional(), Length(min=3, max=20)])
	key_features=TextAreaField('Products Key Features', validators=[Optional()])
	warranty=StringField('Warranty', validators=[ Optional(), Length(min=3, max=20)])
	garantee=StringField('Garantee', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Edit product Info')
