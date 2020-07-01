from flask import render_template, redirect, Blueprint, request, url_for, flash, abort, session as period
from .forms import AddressForm, AccountForm, RegistrationForm, LoginForm, ContactForm, AddToCartForm
from flask_login import current_user, login_user, logout_user, login_required
from Application.database.model import Customer, session
from Application.database.model import ProductDetails, Product, Category, SubCategory, AddToCart, Customer,HomeCategoriesOrder,HomeSlideShowImages
from Application.utils.handle_files import *
from Application.utils.paginate import Paginate
from Application import redis
from sqlalchemy.orm import lazyload
import json

customers=Blueprint('customers', __name__)

@app.before_first_request
def before_request():
	categories = session.query(Category)\
	.options(
		lazyload("sub_category")\
		.lazyload("product")
		).all()
	c = [x.serialize() for x in categories]
	period["categories_menu"] = c

	cart_items = []
	try:
		cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
	except:
		pass
	period["cart_len"] = len(cart_items)


@customers.route("/")
@customers.route('/home')
def home():
	form=LoginForm()
	# cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
	if request.method == "GET":
		images = session.query(HomeSlideShowImages)\
		.order_by(HomeSlideShowImages.order).all()

		ordered_categories = Category.getHomeDisplayCategories(Category)
		page_number = request.args.get("page",1, type=int)
		pages = Paginate(
			ProductDetails.read_products_details(ProductDetails),
			page_number,
			10
		)
		prev_url = url_for("customers.home", page=pages.previous_page) if pages.has_previous else None
		next_url = url_for("customers.home", page=pages.next_page) if pages.has_next else None
	return render_template(
		'customer/index.html', 
		form=form, pages=pages, 
		next_url=next_url, 
		prev_url=prev_url, 
		images=images, 
		enumerate=enumerate,
		ordered_categories=ordered_categories)

@customers.route('/register', methods=["GET", "POST"])
def register():
	form=RegistrationForm()     
	if form.validate_on_submit():
		if form.profile_picture.data:
			#save profile picture
			profile_picture = save_picture(form.profile_picture.data,"static/customer_profile_pictures",125,125)

			#save customer details.
			Customer(
				name = " ".join([form.firstname.data, form.lastname.data]),
				email = form.email.data,
				contact = form.tel.data,
				country = form.countries.data,
				city = form.district.data,
				picture_file_name = profile_picture,
				user_name = form.username.data,
				password = form.confirm_password.data
			)
			flash("Your details have been stored successfully!!", "success")
			return redirect(url_for("customers.login"))
		else:
			#set default picture
			default="commerce.png"
			Customer(
				name = " ".join([form.firstname.data, form.lastname.data]),
				email = form.email.data,
				contact = form.tel.data,
				country = form.countries.data,
				city = form.district.data,
				picture_file_name = default,
				user_name = form.username.data,
				password = form.confirm_password.data
			)
			flash("Your details have been stored successfully!!", "success")
			return redirect(url_for("customers.login"))

	return render_template('customer/register.html', form=form)

@customers.route('/login', methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("customers.home"))
	form=LoginForm()
	if form.validate_on_submit():
		customer = session.query(Customer).filter_by(email=form.email.data).first()
		if customer:
			if customer.verify_password(form.password.data):
				period['account_type'] = 'customer'
				login_user(customer)
				flash("You have been Logged in!!", "success")
				return redirect(url_for("customers.home"))

			else:
				flash('Login not successful. Please check your email and password', 'danger')
				return redirect(url_for("customers.login"))
		else:
			flash('User does not exist. You must create an account to access the site', 'info')
			return redirect(url_for("customers.login"))
	return render_template('customer/login.html', form=form)

@customers.route('/logout')
def logout():
	logout_user()
	period.pop('account_type', None)
	return redirect(url_for("customers.login"))
	
@customers.route("/product_details/<id>", methods=["GET", "POST"]) 
@login_required
def product_details(id):
	form=AddToCartForm()

	if request.method == "GET":
		pdt = ProductDetails.read_product_details(ProductDetails, id)
		product_key = "product-%s"%pdt.prod_details_id
		redis.set(
			product_key, 
			json.dumps(pdt.serialize())
			)
		redis.expire(product_key, 600)
		keys_live = redis.keys("product-*")
		recently_viewed = [
			json.loads(redis.get(k)) for k in keys_live
			]
		sub_cat = pdt.product.sub_category
		cat = sub_cat.category
		products_same_sub_cat = ProductDetails.products_same_sub_cat(ProductDetails,sub_cat.sub_category_id)
		form.product_image.data = pdt.front_picture
		form.product_name.data = pdt.product.name
		if pdt.promotional_price:
			form.unit_price.data = pdt.promotional_price
		else:
			form.unit_price.data = pdt.prize
		if pdt.color:
			form.color.choices = [(color,color) for color in pdt.color.split(',')]
		else:
			pass
		if pdt.size:
			form.size.choices = [(size,size) for size in pdt.size.split(',')]
		else:
			pass
		if pdt.weight:
			form.weight.choices = [(weight,weight) for weight in pdt.weight.split(',')]
		else:
			pass
		return render_template(
			'customer/detail.html', 
			form=form, 
			pdt=pdt, 
			sub_category=sub_cat.name, 
			category=cat.name, 
			you_may_like=products_same_sub_cat, 
			recently_viewed=recently_viewed
			)
	
	elif request.method == "POST":
		if form.quantity.data and form.unit_price.data and form.product_image.data and form.product_name.data:
			pdt = ProductDetails.read_product_details(ProductDetails, id)
			if form.quantity.data > pdt.quantity:
				flash("You specified more than is available","info")
				return redirect(url_for("customers.product_details", id=id))
			else:
				if pdt.promotional_price:          
					customer = Customer.read_customer(Customer, current_user.id)
					AddToCart(form.product_image.data,form.product_name.data,form.quantity.data,pdt.promotional_price,form.size.data,form.color.data,form.weight.data,customer)
					cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
					period["cart_len"] = len(cart_items)
					flash("Product added successfully to the Cart", "success")  
					return redirect(url_for("customers.product_details", id=id))
				else:
					customer = Customer.read_customer(Customer, current_user.id)
					AddToCart(form.product_image.data,form.product_name.data,form.quantity.data,form.unit_price.data,form.size.data,form.color.data,form.weight.data,customer)
					cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
					period["cart_len"] = len(cart_items)
					flash("Product added successfully to the Cart", "success")  
					return redirect(url_for("customers.product_details", id=id))

		else:
			flash("Please fill the specification form in order to get the right product!!", "info")
			return redirect(url_for("customers.product_details", id=id))


@customers.route("/delete_from_cart/<id>", methods=["GET"])
def delete_from_cart(id):
	AddToCart.delete_cart_item(AddToCart, id)
	cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
	period["cart_len"] = len(cart_items)
	flash("Item removed from cart successfully", "success")
	return redirect(url_for('customers.basket'))

@customers.route("/contact", methods=["GET"])  
def contact():
	return render_template('customer/contact.html')

@customers.route("/order")
@login_required
def order():
	return render_template('customer/customer-order.html')

@customers.route("/orders")
@login_required
def orders():
	customer = current_user
	orders = customer.order
	return render_template('customer/customer-orders.html', orders=orders)

	
@customers.route("/recently_viewed")
@login_required
def getrecentlyViewed():
	keys_live = redis.keys("product-*")
	recently_viewed = [
		json.loads(redis.get(k)) for k in keys_live
		]
	return render_template('customer/category.html', products=recently_viewed)

@customers.route("/category")
@login_required
def category():
	category_name = request.args.get("name")
	products = Category.getAllProductsUnderSameCategory(Category, category_name)

	return render_template('customer/category.html', products=products, category_name=category_name)

@customers.route("/sub_cat/<id>")
@login_required
def sub_category(id):
	sub_cat_name = SubCategory.read_sub_category(SubCategory, id)
	products = Category.getAllProductsUnderSameSubCategory(Category, id)

	return render_template('customer/category.html', products=products, sub_cat_name=sub_cat_name.name)


@customers.route("/basket")
@login_required
def basket():
	cart_items = AddToCart.read_customer_cart_items(AddToCart, current_user.id)
	return render_template('customer/basket.html', cart_items=cart_items, cart_len=len(cart_items))

@customers.route("/checkout1", methods=['POST','GET'])
@login_required
def checkout1():
	form=AddressForm()
	return render_template('customer/checkout1.html', form=form)

@customers.route("/checkout2",  methods=['POST','GET'])
@login_required
def checkout2():
	return render_template('customer/checkout2.html')

@customers.route("/checkout3",  methods=['POST','GET'])
@login_required
def checkout3():  
	return render_template('customer/checkout3.html')

@customers.route("/checkout4",  methods=['POST','GET'])
@login_required
def checkout4():
	return render_template('customer/checkout4.html')

@customers.route("/customer-account")
@login_required
def customer_account():
	form=AccountForm()
	return render_template('customer/customer-account.html', form=form)

