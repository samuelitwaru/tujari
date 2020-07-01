from flask import render_template, redirect, Blueprint
from amobit.vendors.forms import AddProduct, RegistrationForm, BusinessForm, LoginForm, AddStock, EditProductForm
vendors=Blueprint('vendors', __name__)


@vendors.route('/vendor/product_upload', methods=['POST', 'GET'])
def product_upload():
	form=AddProduct()
	return render_template('vendor/product-upload.html', form=form)

@vendors.route('/vendor/sales')
def sales():
	return render_template('vendor/sales.html')

@vendors.route('/vendor/login')
def login():
	form=LoginForm()
	return render_template('vendor/login.html', form=form)

@vendors.route('/vendor/listing-product')
def product():
	return render_template('vendor/listed-products.html')


@vendors.route('/vendor/register', methods=['POST', 'GET'])
def register():
	form=RegistrationForm()
	return render_template('vendor/service-provider-register1.html', form=form)

@vendors.route('/vendor/register-step2', methods=['POST', 'GET'])
def register1():
	form=BusinessForm()
	return render_template('vendor/service-provider-register2.html', form=form)

@vendors.route('/vendor/register-step3', methods=['POST', 'GET'])
def register2():
	return render_template('vendor/service-provider-register3.html')

@vendors.route('/vendor/register-summary', methods=['POST', 'GET'])
def summary():
	return render_template('vendor/register-summary.html')

@vendors.route('/vendor/tracking_products')
def products():
	return render_template('vendor/tracking.html')

@vendors.route('/vendor/product_details', methods=['POST', 'GET'])
def product_details():
	form=AddStock()
	return render_template('vendor/product-detail-vendor.html', form=form)

@vendors.route('/vendor/edit_product', methods=['POST', 'GET'])
def edit_product():
	form=EditProductForm()
	return render_template('vendor/edit_product.html', form=form)