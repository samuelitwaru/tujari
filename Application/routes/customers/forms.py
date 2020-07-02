from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField,\
					 SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, ValidationError, Email, EqualTo
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user


class AddressForm(FlaskForm):
	first_name=StringField('First Name', validators=[DataRequired(), InputRequired()])
	last_name=StringField('Last Name', validators=[DataRequired(), InputRequired()])
	street=StringField('Street', validators=[DataRequired(), InputRequired()])
	zipcode=StringField('Zip', validators=[DataRequired(), InputRequired()])
	state=SelectField('District', validators=[DataRequired()], choices=[("Arua", "Arua"), ("Kampala", "Kampala"), ("Tororo","Tororo")])
	country=SelectField('Country', validators=[DataRequired()], choices=[("Uganda", "Uganda"), ("Kenya","Kenya"), ("Tanzania", "Tanzania"),("Rwanda","Rwanda")])
	telephone=StringField('Telephone', validators=[DataRequired(), InputRequired(), Length(min=10, max=13)])
	email=StringField('Email', validators=[Email(), InputRequired()])
	submit=SubmitField('Save Address')

class AccountForm(FlaskForm):
	firstname=StringField('First Name', validators=[DataRequired(), InputRequired()])
	lastname=StringField('Last Name', validators=[DataRequired(), InputRequired()])
	company=StringField('Company', validators=[DataRequired(), InputRequired()])
	street=StringField('Street', validators=[DataRequired(), InputRequired()])
	zipcode=StringField('Zip', validators=[DataRequired(), InputRequired()])
	state=SelectField('State', validators=[DataRequired()], choices=[])
	country=SelectField('Country', validators=[DataRequired()], choices=[])
	tel=StringField('Telephone', validators=[DataRequired(), InputRequired()])
	email=StringField('Email', validators=[Email(), InputRequired()])
	submit=SubmitField('Save changes')

class RegistrationForm(FlaskForm):
	firstname=StringField('First Name', validators=[ InputRequired(), Length(min=3, max=20)])
	lastname=StringField('Last Name', validators=[ InputRequired(), Length(min=3, max=20)])
	username=StringField('Username', validators=[ InputRequired(), Length(min=3, max=20)])
	email=StringField('Email', validators=[ InputRequired(), Email()])
	tel=StringField('Telephone', validators=[InputRequired(), Length(min=10, max=13)])
	password=PasswordField('Password',validators=[ InputRequired(), Length(min=3, max=30)])
	confirm_password=PasswordField('Confirm password',validators=[InputRequired(), EqualTo('password')])
	countries=SelectField('Countries', validators=[InputRequired()], choices=[("Kenya","Kenya"), ("Uganda", "Uganda"), ("Rwanda", "Rwanda"), ("Tanzania", "Tanzania")])
	district=SelectField('District', validators=[InputRequired()], choices=[("Arua","Arua"), ("Nebbi", "Nebbi"), ("Yumbe", "Yumbe"), ("Koboko", "Koboko")])
	profile_picture=FileField('Select Profile Picture', validators=[InputRequired(),FileAllowed(['jpg', 'png'])])
	submit=SubmitField('Sign-up')


class LoginForm(FlaskForm):
	email=StringField('Email', validators=[Email(), InputRequired()])
	password=PasswordField('Password',validators=[ InputRequired(), Length(min=3, max=30)])
	submit=SubmitField('Login')

class ContactForm(FlaskForm):
	firstname=StringField('First Name', validators=[DataRequired(), InputRequired()])
	lastname=StringField('Last Name', validators=[DataRequired(), InputRequired()])
	email=StringField('Email', validators=[Email(), InputRequired()])
	subject=StringField('Subject', validators=[DataRequired(), InputRequired()])
	message=TextAreaField('Message', validators=[DataRequired(), InputRequired()])
	submit=SubmitField('Send Message')

class AddToCartForm(FlaskForm):
	product_name=StringField("Product Name", validators=[InputRequired()])
	product_image=StringField("Product Image", validators=[InputRequired()])
	size=RadioField('Size', validators=[ InputRequired()])
	color=RadioField('Color', validators=[ InputRequired()])
	quantity=IntegerField(validators=[InputRequired()])
	unit_price=IntegerField(validators=[InputRequired()])
	weight=RadioField('weight', validators=[ Optional()])
	submit=SubmitField('submit')

class UpdateCustomerForm(FlaskForm):
	name = StringField("Name", validators=[InputRequired()])
	email = StringField("Email", validators=[InputRequired()])
	contact = StringField("Telephone", validators=[InputRequired()])
	country = SelectField('Country', validators=[InputRequired()], choices=[("Kenya","Kenya"), ("Uganda", "Uganda"), ("Rwanda", "Rwanda"), ("Tanzania", "Tanzania")])
	city = StringField("City", validators=[InputRequired()])
	submit=SubmitField('Update')

class UpdatePasswordForm(FlaskForm):
	current = PasswordField('Current Password', validators=[ InputRequired(), Length(min=3, max=30)])
	new = PasswordField('New Password', validators=[ InputRequired(), Length(min=3, max=30)])
	repeat = PasswordField('Repeat Password', validators=[ InputRequired(), Length(min=3, max=30), EqualTo('new')])
	submit=SubmitField('Update')

	def validate_current(form, field):
		customer = current_user
		if not customer.verify_password(field.data):
			raise ValidationError('Incorrect current password.')