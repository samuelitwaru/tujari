from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField,\
					 SelectField, FloatField, FileField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, ValidationError, Email, EqualTo
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed
from Application.database.model import Category, SubCategory, Brand,session


class RegistrationForm(FlaskForm):
	vendor_name=StringField('Full Name', validators=[ InputRequired(), Length(min=3, max=20)])
	user_name=StringField('User Name', validators=[ InputRequired(), Length(min=3, max=20)])
	vendor_pic=FileField('Vendor pic', validators=[FileAllowed(['jpg', 'png'])])
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
	location=TextAreaField('Address', validators=[ InputRequired(), Length(min=20, max=500)])
	description=TextAreaField('Shop/Company Description', validators=[ InputRequired(), Length(min=20, max=500)])
	license_number=StringField('License Number', validators=[ Optional(), Length(min=3, max=20)])
	other_files=FileField('', validators=[FileAllowed(['pdf'])])
	contact=StringField('Tel Number:', validators=[ InputRequired(), Length(min=3, max=20)])
	submit=SubmitField('Continue to Payment Details')

class LoginForm(FlaskForm):
	email=StringField('Email', validators=[Email(), InputRequired()])
	password=PasswordField('Password',validators=[ InputRequired(), Length(min=3, max=30)])
	submit=SubmitField('Login')

class AddProduct(FlaskForm):
	name=StringField('Name', validators=[ InputRequired(), Length(min=3, max=20)])
	category=SelectField('Category Name', validators=[ InputRequired()], choices=[(category.name, category.name) for category in session.query(Category).all()])
	sub_category=SelectField('Sub_Category Name', validators=[ InputRequired()], choices=[(sub_cat.name,sub_cat.name) for sub_cat in session.query(SubCategory).all()])
	brand=SelectField('Brand', validators=[ InputRequired()], choices=[(brand.name,brand.name) for brand in session.query(Brand).all()])
	product_type=StringField('Product Type', validators=[ Optional(), Length(min=3, max=20)])
	size=StringField('Size', validators=[ Optional(), Length(min=3, max=20)])
	color=StringField('Color', validators=[ InputRequired()])
	quantity=StringField('quantity', validators=[ InputRequired(), Length(min=1, max=20)])
	weight=StringField('weight', validators=[ Optional(), Length(min=3, max=20)])
	front_pic=FileField('Front Image', validators=[FileAllowed(['jpg', 'png'])])
	back_pic=FileField('Back Image', validators=[FileAllowed(['jpg', 'png'])])
	description=TextAreaField('Total Product Description', validators=[InputRequired()])
	prize=StringField('Price', validators=[ Optional(), Length(min=3, max=20)])
	key_features=TextAreaField('Products Key Features', validators=[Optional()])
	warranty=StringField('Warranty', validators=[ Optional(), Length(min=3, max=20)])
	guarantee=StringField('Guarantee', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Add Product')

class AddStock(FlaskForm):
	quantity=StringField('Add Quantity', validators=[ InputRequired(), Length(min=3, max=20)])
	price=StringField('Promotional Price', validators=[ InputRequired(), Length(min=3, max=20)])
	submit=SubmitField('Add')


class EditProductForm(FlaskForm):  
	name=StringField('Name', validators=[InputRequired(), Length(min=3, max=20)])
	category=StringField('Category Name', validators=[ InputRequired()])
	sub_category=StringField('Sub_Category Name', validators=[ InputRequired()])
	brand=StringField('Brand', validators=[ InputRequired()])
	product_type=StringField('Product Type', validators=[ Optional(), Length(min=3, max=20)])
	size=StringField('Size', validators=[ Optional(), Length(min=3, max=20)])
	color=StringField('Color', validators=[ InputRequired(), Length(min=3, max=20)])
	weight=StringField('weight', validators=[ Optional(), Length(min=3, max=20)])
	front_pic=FileField('Change Front Image', validators=[Optional(),FileAllowed(['jpg', 'png', 'pdf'])])
	back_pic=FileField('Change Back Image', validators=[Optional(),FileAllowed(['jpg', 'png', 'pdf'])])
	description=TextAreaField('Total Product Description', validators=[InputRequired()])
	prize=StringField('Prize', validators=[ Optional(), Length(min=3, max=20)])
	key_features=TextAreaField('Products Key Features', validators=[Optional()])
	warranty=StringField('Warranty', validators=[ Optional(), Length(min=3, max=20)])
	guarantee=StringField('Guarantee', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Edit product Info')


class UpdateVendorForm(FlaskForm):
	vendor_name = StringField("Name", validators=[ InputRequired(), Length(min=3, max=20)])
	address = StringField("Address", validators=[Optional()])
	email = StringField("Email", validators=[InputRequired(), Email()])
	contact = StringField("Telephone", validators=[ InputRequired(), Length(min=3, max=20)])
	submit=SubmitField('Save')

class UpdateVendorBusinessForm(FlaskForm):
	shop_name=StringField('Shop Name', validators=[ Optional(), Length(min=3, max=20)])
	company_name=StringField('Company Name', validators=[ Optional(), Length(min=3, max=20)])
	location=TextAreaField('Address', validators=[ InputRequired(), Length(min=20, max=500)])
	description=TextAreaField('Shop/Company Description', validators=[ InputRequired(), Length(min=20, max=500)])
	tin_number=StringField('TIN Number', validators=[ Optional(), Length(min=3, max=20)])	
	license_number=StringField('License Number', validators=[ Optional(), Length(min=3, max=20)])
	submit=SubmitField('Save')


class UpdatePasswordForm(FlaskForm):
	current = PasswordField('Current Password', validators=[ InputRequired(), Length(min=3, max=30)])
	new = PasswordField('New Password', validators=[ InputRequired(), Length(min=3, max=30)])
	repeat = PasswordField('Repeat Password', validators=[ InputRequired(), Length(min=3, max=30), EqualTo('new')])
	submit=SubmitField('Update')

	def validate_current(field, form):
		if field.data != current_user.password:
			raise ValidationError('Incorrect current password.')


class UpdateVendorImageForm(FlaskForm):
	vendor_pic_file_name=FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])


class UpdateVendorFileForm(FlaskForm):
	additional_file_names = FileField('Vendor File', validators=[FileAllowed(['pdf']), DataRequired()])
	submit=SubmitField('Save')