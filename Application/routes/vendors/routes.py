from flask import render_template, redirect, Blueprint, request, url_for, flash, abort, session as period, send_from_directory
from Application import app
from Application.database.model import Shop,SubCategory,Product,ProductDetails,Category,TrackProducts,session
from .forms import AddProduct, RegistrationForm, BusinessForm, LoginForm, AddStock, EditProductForm
import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from Application.utils.paginate import Paginate
from Application.utils.handle_files import *

from random import randint

vendors=Blueprint('vendors', __name__)
vendor_details = {
	'full_names':'', 
	'user_name': '',
	'vendor_pic':'',
	'email':'',
	'address':'',
	'password':'',
	'confirm_password':'',
	'contact':'',
	'tin_number':'',
	'shop_name':'',
	'company_name':'',
	'location':'',
	'description':'',
	'license_number':'',
	'other_files':'',
	'second_contact':''
	}

@vendors.route('/vendor/product_upload', methods=['POST', 'GET'])
@login_required
def product_upload():  
	form=AddProduct()
	if form.validate_on_submit():
		sub_category = session.query(SubCategory).filter_by(name=form.sub_category.data).first()
		shop = session.query(Shop).filter_by(id=current_user.id).first()
		if sub_category:
			#save product
			product = Product(form.name.data,sub_category,shop)
			if product:
				#upload photo to the server
				front_picture = save_picture(form.front_pic.data,"static/vendor_product_pictures",800,800)
				back_picture = save_picture(form.back_pic.data,"static/vendor_product_pictures",800,800)
				#save product details
				ProductDetails(
					product_type=form.product_type.data,
					brand=form.brand.data,
					color=form.color.data,
					size=form.size.data,
					front_picture=front_picture,
					back_picture=back_picture,
					key_features=form.key_features.data,
					quantity=form.quantity.data,
					prize=form.prize.data,
					weight=form.weight.data,
					description=form.description.data,
					warranty=form.warranty.data,
					guarantee=form.guarantee.data,
					product=product
				)
				flash("Your product has been saved successfully!!", "success")
				return redirect(url_for("vendors.product_upload"))
	return render_template('vendor/product-upload.html', form=form)


@vendors.route('/vendor/sales')
@login_required
def sales():
	return render_template('vendor/sales.html')

@vendors.route('/vendor/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("vendors.product_upload"))
	form=LoginForm()  
	if form.validate_on_submit():
		vendor = session.query(Shop).filter_by(email=form.email.data).first()
		if vendor:
			if vendor.verify_password(form.password.data):
				period['account_type'] = 'vendor'
				login_user(vendor)
				flash("You have been Logged in!", "success")
				return redirect(url_for("vendors.sales"))
			else:
				flash('Login not successful. Please check your email and password', "danger")
				return redirect(url_for("vendors.login"))
		else:
			flash('User does not exist. You must create an account to access the site', "info")
			return redirect(url_for("vendors.login"))

	return render_template('vendor/login.html', form=form)

@vendors.route('/vendor/logout')
def logout():
	logout_user()
	period.pop('account_type', None)
	return redirect(url_for("vendors.login"))

@vendors.route('/vendor/listing-product', methods=['GET'])
@login_required
def product():
	if request.method == "GET":
		page_number = request.args.get("page",1, type=int)
		pages = Paginate(
			ProductDetails.read_products_details(ProductDetails),
			page_number,
			10
		)
		prev_url = url_for("vendors.product", page=pages.previous_page) if pages.has_previous else None
		next_url = url_for("vendors.product", page=pages.next_page) if pages.has_next else None


	return render_template('vendor/listed-products.html', pages=pages, next_url=next_url, prev_url=prev_url)


@vendors.route('/vendor/register', methods=['POST', 'GET'])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		#first step
		vendor_details['full_names'] = form.vendor_name.data
		vendor_details['user_name'] = form.user_name.data
		vendor_details['email'] = form.email.data
		vendor_details['address'] = form.address.data
		vendor_details['password'] = form.password.data
		vendor_details['confirm_password'] = form.confirm_password.data
		vendor_details['contact'] = form.contact.data
		terms = form.check.data
		if terms:
			#save profile picture
			profile_pic = save_picture(form.vendor_pic.data,'static/profile_pics',125,125)
			vendor_details['vendor_pic'] = profile_pic
			#redirect to second step  
			return redirect(url_for("vendors.register1"))
		else:
			flash("To continue you must agree to our terms and conditions!!!", "error")

	elif request.method == "GET":
		form.vendor_name.data = vendor_details["full_names"]
		form.user_name.data = vendor_details["user_name"]
		form.vendor_pic.data = vendor_details["vendor_pic"]
		form.email.data = vendor_details["email"]
		form.address.data = vendor_details["address"]
		form.password.data = vendor_details["password"]
		form.confirm_password.data = vendor_details["confirm_password"]
		form.contact.data = vendor_details["contact"]

	return render_template('vendor/service-provider-register1.html', form=form)

@vendors.route('/vendor/register-step2', methods=['POST', 'GET'])
def register1():
	form=BusinessForm()
	if form.validate_on_submit():
		#second step 
		vendor_details['tin_number'] = form.tin_number.data
		vendor_details['shop_name'] = form.shop_name.data
		vendor_details['company_name'] = form.company_name.data
		vendor_details['location'] = form.location.data
		vendor_details['description'] = form.description.data
		vendor_details['license_number'] = form.license_number.data
		vendor_details['second_contact'] = form.contact.data

		#save document files
		other_files = save_document(form.other_files.data)
		vendor_details['other_files'] = other_files

		return redirect(url_for("vendors.summary"))

	elif request.method == "GET":
		form.tin_number.data = vendor_details['tin_number']
		form.shop_name.data = vendor_details['shop_name']
		form.company_name.data = vendor_details['company_name']
		form.location.data = vendor_details["location"]
		form.description.data = vendor_details["description"]
		form.license_number.data = vendor_details["license_number"]
		form.other_files.data = vendor_details['other_files']
		form.contact.data = vendor_details['second_contact']
		


	return render_template('vendor/service-provider-register2.html', form=form)

@vendors.route('/vendor/register-step3', methods=['POST', 'GET'])
def register2():
	return render_template('vendor/service-provider-register3.html')

@vendors.route('/vendor/register-summary', methods=['POST', 'GET'])
def summary():
	if request.method == "POST":
		if request.form.get('check'):
			for key in vendor_details:
				if vendor_details[key] == '':
					print("Missing details!!")
					return redirect(url_for('vendors.register'))
			Shop(
				vendor_name=vendor_details['full_names'],
				vendor_pic_file_name=vendor_details['vendor_pic'],
				user_name=vendor_details['user_name'], 
				password=vendor_details['password'],
				address=vendor_details['address'],
				email=vendor_details['email'],
				contact=vendor_details['contact'],
				shop_name=vendor_details['shop_name'],
				company_name=vendor_details['company_name'],  
				location=vendor_details['location'],
				description=vendor_details['description'],
				tin_number=vendor_details['tin_number'],
				license_number=vendor_details['license_number'],
				additional_file_names=vendor_details['other_files'],
				second_contact=vendor_details['second_contact']  
			)
			flash("Your details have been stored successfully!", "success")
			return redirect(url_for("vendors.login"))

	return render_template('vendor/register-summary.html', vendor_details=vendor_details)

@vendors.route('/vendor/tracking_products')
@login_required
def products():
	return render_template('vendor/tracking.html')

@vendors.route('/vendor/product_details/<id>')
@login_required
def product_details(id):
	form = AddStock()
	if request.method == "GET":
		product = ProductDetails.read_product_details(ProductDetails, id)
		return render_template('vendor/product-detail-vendor.html',form=form, product=product)

@vendors.route('/vendor/add_stock/<id>', methods=["POST"])
@login_required
def add_stock(id):
	if request.method == "POST":
		product = ProductDetails.read_product_details(ProductDetails, id)
		if product:
			#increase stock
			try:
				quantity = int(request.form['quantity'])
				ProductDetails.increase_stock(ProductDetails, product.prod_details_id, quantity)
				# TrackProducts(quantity, product)
				flash("Product stock increased successfully!!", "success")
				return redirect(url_for("vendors.product_details", id=id))
			except ValueError:
				flash("Must be a number e.g 1.", "info")
				return redirect(url_for("vendors.product_details", id=id))
		else:
			flash("Product doesnot exists!!", "error")
			return redirect(url_for("vendors.product_details", id=id))

@vendors.route('/vendor/set_promotional_price/<id>', methods=["POST"])
@login_required
def set_promo_price(id):
	form = AddStock()
	if request.method == "POST":
		product = ProductDetails.read_product_details(ProductDetails, id)
		#check if product exists
		if product:
			# adding promotional price
			try:
				promotional_price = int(form.price.data)
				ProductDetails.set_promotional_price(ProductDetails, product.prod_details_id, promotional_price)
				flash("Promotional price has been set up successfully!!", "success")
				return redirect(url_for("vendors.product_details", id=id))

			except ValueError:
				flash("Must be a number e.g 1000.", "info")
				return redirect(url_for("vendors.product_details", id=id))
		else:
			flash("Product doesnot exists!!", "error")
			return redirect(url_for("vendors.product_details", id=id))  


@vendors.route('/vendor/delete_product/<id>', methods=["GET"])
@login_required
def delete_product(id):
	if request.method == "GET":
		#delete product and it's details.
		ProductDetails.delete_product_details(ProductDetails, id)
		flash("Product deleted successfully!!", "success")
		return redirect(url_for("vendors.sales"))
	else:
		abort(403)

@vendors.route('/vendor/edit_product/<id>', methods=['POST', 'GET'])
def edit_product(id):
	form=EditProductForm()
	if request.method == "GET":
		product = ProductDetails.read_product_details(ProductDetails, id)
		sub_cat = product.product.sub_category
		cat = sub_cat.category
		form.name.data = product.product.name
		form.category.data = cat.name
		form.sub_category.data = sub_cat.name
		form.brand.data = product.brand
		form.product_type.data = product.product_type
		form.size.data = product.size
		form.color.data = product.color
		form.weight.data = product.weight
		form.description.data = product.description
		form.prize.data = product.prize
		form.key_features.data = product.key_features
		form.warranty.data = product.warranty
		form.guarantee.data = product.guarantee
		return render_template('vendor/edit_product.html', form=form, front_pic=product.front_picture, back_pic=product.back_picture, id=id)
  
	elif request.method == "POST":
		if form.validate_on_submit():
			#update product details
			if form.front_pic.data and form.back_pic.data:
				front_picture = save_picture(form.front_pic.data,"static/vendor_product_pictures",800,800)
				back_picture = save_picture(form.back_pic.data,"static/vendor_product_pictures",800,800)
				product = ProductDetails.read_product_details(ProductDetails, id)
				Product.update_product(Product,product.product_id,form.name.data) 
				ProductDetails.update_product_details(
					ProductDetails,
					id,
					form.brand.data,
					form.product_type.data,
					form.size.data,
					form.color.data,
					form.weight.data,
					form.key_features.data,
					form.description.data,
					form.prize.data,
					form.warranty.data,
					form.guarantee.data,
					front_picture,
					back_picture
				)
				flash("Product has been updated successfully!!", "success")
				return redirect(url_for("vendors.edit_product", id=id))
			else:
				product = ProductDetails.read_product_details(ProductDetails, id)
				Product.update_product(Product,product.product_id,form.name.data) 
				ProductDetails.update_product_details(
					ProductDetails,
					id,
					form.brand.data,
					form.product_type.data,
					form.size.data,
					form.color.data,
					form.weight.data,
					form.key_features.data,
					form.description.data,
					form.prize.data,
					form.warranty.data,
					form.guarantee.data,
					product.front_picture,
					product.back_picture
				)
				flash("Product has been updated successfully!!", "success")
				return redirect(url_for("vendors.edit_product", id=id))
		else:
			flash("Form not validated well!!", "info")
			return redirect(url_for("vendors.edit_product", id=id))

@vendors.route('/track_products', methods=["GET"])
def track_products():
	return render_template('vendor/track_products.html')

@vendors.route("/file1/<path:file_name>", methods=["POST", "GET"])
def getfile(file_name):
	return redirect(url_for("static",filename="vendor_product_pictures/"+file_name))

@vendors.route("/file4/<path:file_name>", methods=["POST", "GET"])
def getVendorfile(file_name):
	return redirect(url_for("static",filename="vendor_documents/"+file_name))

@vendors.route("/file5/<path:file_name>", methods=["POST", "GET"])
def getProfilePicfile(file_name):
	return redirect(url_for("static",filename="profile_pics/"+file_name))

@vendors.route("/file2/<path:file_name>", methods=["POST", "GET"])
def downloadfile(file_name):
	directory = os.path.realpath(".") +"/Application/static/vendor_product_pictures"
	print("Directory:",directory)
	return send_from_directory(directory=directory,filename=file_name)

@vendors.route("/file3/<path:file_name>", methods=["POST", "GET"])
def downloadVendorfile(file_name):
	directory = os.path.realpath(".") + "/Application/static/vendor_documents"
	return send_from_directory(directory,file_name)

@vendors.route("/file6/<path:file_name>", methods=["POST", "GET"])
def downloadProfilePicfile(file_name):
	directory = os.path.realpath(".") + "/Application/static/profile_pics"
	return send_from_directory(directory,file_name)


