from sqlalchemy import (
    Column,
    ForeignKey,
    BigInteger,
    Float,
    Enum,
    String,
    DateTime,
    Boolean,
    Integer,
    create_engine,
    exc,
    func
)
from flask_login import UserMixin
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import relationship, sessionmaker, column_property
from sqlalchemy.orm import sessionmaker, scoped_session, lazyload
from Application import app, login_manager
from passlib.context import CryptContext
from werkzeug.security import generate_password_hash, check_password_hash
from os import remove, path
from datetime import datetime
from flask import session as period

pwd_context = CryptContext(  
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)
  

basedir = path.abspath(path.dirname(__file__))
pth = 'sqlite:///' + path.join(basedir, 'database.db')
engine = create_engine(pth,connect_args={'check_same_thread': False},echo=False)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base(bind=engine)
Base.query = session.query_property()
@login_manager.user_loader
def load_user(user_id):
    if period['account_type'] == 'vendor':
        return session.query(Shop).filter_by(id=user_id).first()
    elif period['account_type'] == 'customer':
        return session.query(Customer).filter_by(id=user_id).first()
    elif period['account_type'] == 'admin':
        print("Administrator")
    else:
        return None

class Shop(Base, UserMixin):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    vendor_name = Column(String)
    vendor_pic_file_name = Column(String)
    user_name = Column(String, index=True, unique=True)
    password = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    contact = Column(String, unique=True)
    shop_name = Column(String)
    company_name = Column(String)
    location = Column(String)
    description = Column(String)
    date_of_registration = Column(DateTime, default=datetime.now())
    tin_number = Column(String)
    license_number = Column(String)
    additional_file_names = Column(String)
    second_contact = Column(String, unique=True)

    def __init__(self, vendor_name,vendor_pic_file_name,user_name,password,
        address,email,contact,shop_name,company_name,location,description,
        tin_number,license_number,additional_file_names,second_contact):
        self.vendor_name = vendor_name
        self.vendor_pic_file_name = vendor_pic_file_name
        self.user_name = user_name
        self.hash_password(password)
        self.address = address
        self.email = email
        self.contact = contact
        self.shop_name = shop_name
        self.company_name = company_name
        self.location = location
        self.description = description
        self.tin_number = tin_number
        self.license_number = license_number
        self.additional_file_names = additional_file_names
        self.second_contact = second_contact

        try:
            session.add(self)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return None

    def read_vendor(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_vendors(self):
        return session.query(self).all()

    def delete_vendor(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()

    def update_vendor(self,id,vendor_name,vendor_pic_file_name,address,city,email,contact,shop_name,description,tin_number,license_number):
        vendor = session.query(self).filter_by(id=id).first()
        vendor.vendor_name = vendor_name
        vendor.vendor_pic_file_name = vendor_pic_file_name
        vendor.address = address
        vendor.city = city
        vendor.email = email
        vendor.contact = contact
        vendor.shop_name = shop_name
        vendor.description = description
        vendor.tin_number = tin_number
        vendor.license_number = license_number

        session.commit()
        

    def verify_password(self, password):
        return check_password_hash(self.password,password)


    def hash_password(self, password):
        self.password = generate_password_hash(password)


class Customer(Base,  UserMixin):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String)   
    email = Column(String, unique=True)
    contact = Column(String, unique=True)
    country = Column(String)
    city = Column(String)
    picture_file_name = Column(String)
    user_name = Column(String, unique=True)
    password = Column(String)
    date_of_registration = Column(DateTime, default=datetime.now())
    

    def __init__(self,name,email,contact,country,city,picture_file_name,user_name,password):
        self.name = name
        self.email = email
        self.contact = contact
        self.country = country
        self.city = city
        self.picture_file_name = picture_file_name
        self.user_name = user_name
        self.hash_password(password)

        try:
            session.add(self)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return None

    def read_customer(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_customers(self):
        return session.query(self).all()

    def update_customer(self,id,name,email,contact,country,city,picture_file_name):
        customer = session.query(self).filter_by(id=id).first()
        customer.name = name
        customer.email = email
        customer.contact = contact
        customer.country = country
        customer.city = city
        customer.picture_file_name = picture_file_name

        session.commit()

    def delete_customer(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()


    def verify_password(self, password):
        return check_password_hash(self.password,password)

    def hash_password(self, password):
        self.password = generate_password_hash(password)


class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        try:
            self.name = name
            session.add(self)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return None

    def read_category(self, id):
        return session.query(self).filter_by(category_id=id).first()

    def read_categories(self):
        return session.query(self).all()

    def update_category(self,id,name):
        category = session.query(self).filter_by(id=id).first()
        category.name = name
        session.commit()

    def delete_category(self,id):
        session.query(self).filter_by(id=id).delete()
        session.commit()
    
    def getHomeDisplayCategories(self): # gets 5 products per category
        categories_display = {}
        ordered_categories = session.query(self)\
            .join(Category.home_categories_order)\
            .filter(self.category_id == HomeCategoriesOrder.category_id)\
            .order_by(HomeCategoriesOrder.order)\
            .options(lazyload("sub_category"))\
            .all()

        for category in ordered_categories:
            subcategories = category.sub_category
            for subcategory in subcategories:
                products = session.query(ProductDetails)\
                    .join(ProductDetails.product)\
                    .filter(
                        Product.sub_category_id == subcategory.sub_category_id
                        )\
                    .all()
                if products:
                    for product in products:
                        if product != None:
                            if category.name in categories_display:
                                if len(categories_display[category.name]) != 5:
                                    categories_display[category.name]\
                                    .append(product)
                            else:
                                categories_display[category.name] = [product]

        return categories_display

    def getAllProductsUnderSameCategory(self, name): # gets all products under same category
        products_display = []
        category = session.query(self)\
            .filter(self.name == name)\
            .options(lazyload("sub_category"))\
            .first()

        subcategories = category.sub_category
        for subcategory in subcategories:
            products = session.query(ProductDetails)\
                .join(ProductDetails.product)\
                .filter(
                    Product.sub_category_id == subcategory.sub_category_id
                    ).all()
            for product in products:
                if product != None:
                    products_display.append(product)

        return products_display

    def getAllProductsUnderSameSubCategory(self, id):
        products_display = []
        products = session.query(ProductDetails)\
                .join(ProductDetails.product)\
                .filter(
                    Product.sub_category_id == id
                    ).all()
        for product in products:
            if product != None:
                products_display.append(product)
        return products_display

    def serialize(self):
        return {
            "id": self.category_id,
            "name":self.name,
            "sub_category": [ x.serialize() for x in self.sub_category]
        }

class SubCategory(Base):
    __tablename__ = "sub_category"
    sub_category_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    category = relationship("Category", backref="sub_category")

    def __init__(self,name,category):
        try:
            self.name = name
            self.category = category
            session.add(self)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return None

    def add_item_by_id(self,id,name):
        self.__init__(name=name, category=None)
        self.category_id = id
        session.add(self)
        session.commit()

    def read_sub_category(self,id):
        return session.query(self).filter_by(sub_category_id=id).first()

    def read_sub_categories(self):
        return session.query(self).all()

    def update_sub_category(self,id,name):
        update =  session.query(self).filter_by(id=id).update({"name":name})
        if update:
            session.commit()
            return update
        else:
            return False

    def delete_sub_category(self,id):
        session.query(self).filter_by(id=id).delete()
        session.commit()

    def serialize(self):
        return {
            "id": self.sub_category_id,
            "name": self.name,
            "product": [x.serialize() for x in self.product]
        }

class Brand(Base):
    __tablename__ = "brand"
    brand_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self,name):
        try:
            self.name = name
            session.add(self)
            session.commit()
        except exc.IntegrityError:
            session.rollback()
            return None

    def read_brand(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_brands(self):
        return session.query(self).all()

    def update_brand(self,id,name):
        brand = session.query(self).filter_by(id=id).first()
        brand.name = name
        session.commit()

    def delete_brand(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    sub_category_id = Column(Integer, ForeignKey("sub_category.sub_category_id"))
    sub_category = relationship("SubCategory", backref="product")
    shop_id = Column(Integer, ForeignKey("shop.id"))
    shop = relationship("Shop", backref="product")

    def __init__(self,name,sub_category,shop):
        self.name = name
        self.sub_category = sub_category
        self.shop = shop
        session.add(self)
        session.commit()

    def read_product(self, id):
        return session.query(self).filter_by(product_id=id).first()

    def read_products(self):
        return session.query(self)

    def read_vendor_products(self, id):
        return session.query(self).filter_by(shop_id=id)

    def update_product(self,id,name):
        product = session.query(self).filter_by(product_id=id).first()
        product.name = name
        session.commit()

    def delete_product(self,id):
        session.query(self).filter_by(product_id=id).delete()
        session.commit()

    def serialize(self):
        return {
            "id": self.product_id,
            "name": self.name
        }
    

class ProductDetails(Base):
    __tablename__ = "product_details"
    prod_details_id = Column(Integer, primary_key=True)
    product_type = Column(String)
    brand = Column(String)
    color = Column(String)
    size = Column(String)
    front_picture = Column(String)
    back_picture = Column(String)
    key_features = Column(String)
    quantity = Column(Integer)
    prize = Column(Integer)
    weight = Column(Integer)
    description = Column(String)
    warranty = Column(String, default="")
    guarantee = Column(String, default="")
    promotional_price = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.product_id"))
    product = relationship("Product", uselist=False, backref="product_details")

    def __init__(self,product_type,brand,color,size,front_picture,back_picture,key_features,quantity,prize,weight,description,warranty,guarantee,product):
        self.product_type = product_type
        self.brand = brand
        self.color = color
        self.size = size
        self.front_picture = front_picture
        self.back_picture = back_picture
        self.key_features = key_features
        self.quantity = quantity
        self.prize = prize
        self.weight = weight
        self.description = description
        self.warranty = warranty
        self.guarantee = guarantee
        self.product = product
        session.add(self)
        session.commit()

    def read_product_details(self,id):
        return session.query(self).filter_by(prod_details_id=id).first()

    def read_products_details(self):
        return session.query(self)

    def read_products_name_and_image(self):
        return session.query(self.product.name, self.front_picture).all()
    
    def products_same_sub_cat(self, id):
        return session.query(self).join(self.product).filter(Product.sub_category_id == id).order_by(self.prod_details_id).all()


    def update_product_details(self,id,brand,product_type,size,color,weight,key_features,description,price,warranty,guarantee,front_picture,back_picture):
        product = session.query(self).filter_by(prod_details_id=id).first()
        product.brand = brand
        product.product_type = product_type
        product.size = size
        product.color = color
        product.weight = weight
        product.key_features = key_features
        product.description = description
        product.prize = price
        product.warranty = warranty
        product.guarantee = guarantee
        product.front_picture = front_picture
        product.back_picture = back_picture
        session.commit()

    def increase_stock(self, id, quantity):
        product = session.query(self).filter_by(prod_details_id=id).first()
        product.quantity += quantity
        session.commit()

    def set_promotional_price(self, id, promotional_price):
        product = session.query(self).filter_by(prod_details_id=id).first()
        if product:
            product.promotional_price = promotional_price
            session.commit()
        else:
            return None

    def delete_product_details(self,id):
        product = session.query(Product).filter_by(product_id=id).first()
        product_detail_id = product.product_details.prod_details_id
        product_details = session.query(self).filter_by(prod_details_id=product_detail_id).first()
        if product_details:
            dir_path = path.abspath(path.dirname(__file__))
            real_path = dir_path.replace('/database','')
            file_path_front = path.join(real_path + "/static/vendor_product_pictures", product_details.front_picture)
            file_path_back = path.join(real_path + "/static/vendor_product_pictures", product_details.back_picture)
            try:
                remove(file_path_front)
                remove(file_path_back)
                session.query(Product).filter_by(product_id=id).delete()
                session.query(self).filter_by(prod_details_id=product_detail_id).delete()
                session.commit()
            except OSError as e:
                print("Failed with:", e.strerror)
                print("Error code:", e)
            except FileNotFoundError:
                pass
        else:
            return None
    
    def serialize(self):
        return {
            "prod_details_id":self.prod_details_id,
            "product_type": self.product_type, 
            "brand": self.brand,
            "color": self.color,
            "size": self.size,
            "front_picture": self.front_picture,
            "back_picture": self.back_picture,
            "key_features": self.key_features,
            "quantity": self.quantity,
            "prize": self.prize,
            "weight": self.weight,
            "description": self.description,
            "warranty": self.warranty,
            "guarantee": self.guarantee,
            "product":{
                "name": self.product.name
            }
        }

class TrackProducts(Base):
    __tablename__ = "trackproducts"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    date = Column(DateTime, default=datetime.now())
    product_id = Column(Integer, ForeignKey("product.product_id"))
    product = relationship("Product", backref="trackproducts")

    def __init__(self, quantity, product):
        self.quantity = quantity
        self.product = product
        session.add(self)
        session.commit()

    def read_vendor_products(self, shop_id):
        return session.query(Product).filter_by(shop_id=shop_id).all()


class Stock(Base):
    __tablename__ = "stock"
    stock_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    date =  Column(DateTime, default=datetime.now())
    product_details_id = Column(Integer, ForeignKey("product_details.prod_details_id"))
    product_details = relationship("ProductDetails", backref="stock")

    def __init__(self,quantity,product_details):
        self.quantity = quantity
        self.product_details = product_details
        session.add(self)
        session.commit()

    def read_stock(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_stocks(self):
        return session.query(self).all()

    def update_quantity(self,id,quantity):
        stock = session.query(self).filter_by(id=id).first()
        stock.quantity = quantity
        session.commit()

    def delete_stock(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()
    

class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True)
    amount = Column(String)
    quantity = Column(Integer)
    order_date = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=False)
    customer_id=  Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", backref="order")
    product_details_id = Column(String, ForeignKey("product_details.prod_details_id"))
    product_details = relationship("ProductDetails", backref="order")
    

    def __init(self, amount, quantity, customer, product):
        self.amount = amount
        self.quantity = quantity
        self.customer = customer
        self.product_details = product
        session.add(self)
        session.commit()

    def read_order(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_orders(self):
        return session.query(self).all()

    def update_order(self,id,amount,quantity):
        order = session.query(self).filter_by(id=id).first()
        order.amount = amount
        order.quantity = quantity
        session.commit()

    def delete_order(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()
        

class AddToCart(Base):
    __tablename__ = "addtocart"
    id = Column(Integer, primary_key=True)
    product_image = Column(String)
    product_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Integer)
    size = Column(String)
    color = Column(String)
    weight = Column(String)
    date = Column(DateTime, default=datetime.now())
    state = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", backref="addtocart")
    
    def __init__(self,product_image,product_name,quantity,unit_price,size,color,weight,customer):
        self.product_image = product_image
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.size = size
        self.color = color
        self.weight = weight
        self.customer = customer
        session.add(self)
        session.commit()

    def read_cart_item(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_cart_items(self):
        return session.query(self).all()

    def read_customer_cart_items(self, customer_id):
        return [cart_item for cart_item in session.query(self).filter_by(customer_id=customer_id).all() if not cart_item.state]

    def delete_cart_item(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()

class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True)
    payment_date = Column(DateTime, default=datetime.now())
    payment_method = Column(String, Enum("mobile_money", "visa", "cash_on_delivery"))
    order_id = Column(Integer, ForeignKey("order.order_id"))
    order = relationship("Order",uselist=False,backref="payment")

    def __init__(self,payment_method,order):
        self.payment_method = payment_method
        self.order = order
        session.add(self)
        session.commit()

    def read_payment(self, id):
        return session.query(self).filter_by(id=id).first()

    def read_payments(self):
        return session.query(self).all()

    def delete_payment(self, id):
        session.query(self).filter_by(id=id).delete()
        session.commit()

class MobileMoney(Base):
    __tablename__ = "mobile_money"
    transaction_id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.payment_id"))
    payment1 = relationship("Payment", backref="mobile_money")
    name = Column(String)
    email = Column(String)
    amount = Column(Integer)
    contact = Column(String)
    status = Column(String, Enum("pending", "failed", "confirmed"))
    transaction_ref=  Column(String)

class Visa(Base):
    __tablename__ = "visa"
    transaction_id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.payment_id"))
    payment2 = relationship("Payment", backref="visa")
    name = Column(String)
    email = Column(String)
    amount = Column(Integer)
    contact = Column(String)
    account_number = Column(String)
    security_number = Column(Integer)
    expiry_date = Column(String)
    status = Column(String, Enum("pending", "failed", "confirmed"))
    transaction_ref=  Column(String)

class CashOnDelivery(Base):
    __tablename__ = "cash_on_delivery"
    transaction_id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.payment_id"))
    payment3 = relationship("Payment", backref="cash_on_delivery")
    transaction_ref = Column(String)

class Sales(Base):
    __tablename__ = "sales"
    sales_id = Column(Integer, primary_key=True)
    product_details_id = Column(Integer, ForeignKey("product_details.prod_details_id"))
    product_details3 = relationship("ProductDetails", backref="sales")
    quantity = Column(Integer)
    amount = Column(Integer)
    date =  Column(DateTime, default=datetime.now())

class CustomerAddress(Base):
    __tablename__ = "customer_address"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    country = Column(String)
    _zip = Column(String)
    district = Column(String)
    street = Column(String)
    telephone = Column(String)
    email = Column(String)

class Delivery(Base):
    __tablename__ = "delivery"
    delivery_id = Column(Integer, primary_key=True)
    deliverer_name = Column(Integer)
    driver_license_number = Column(String)
    contact = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    carrier_means = Column(String)
    carrier_type = Column(String)
    carrier_license_plate_number = Column(String)

class DeliveryDetails(Base):
    __tablename__ = "delivery_details"
    delivery_details_id = Column(Integer, primary_key=True)
    delivery_id = Column(Integer, ForeignKey("delivery.delivery_id"))
    delivery1 = relationship("Delivery", backref="delivery_details")
    order_id = Column(Integer, ForeignKey("order.order_id"))
    order1 = relationship("Order", backref="delivery_details")
    delivery_address = Column(String)
    delivery_ref_number = Column(String)

class HomeSlideShowImages(Base):
    __tablename__ = "home_slide_show_images"
    image_id = Column(Integer, primary_key=True)
    order = Column(Integer, unique=True)
    image_name = Column(String)
    caption = Column(String)

    def __init__(self, order, image_name, caption):
        self.order = order
        self.image_name = image_name
        self.caption = caption
        session.add(self)
        session.commit()

class HomeCategoriesOrder(Base):
    __tablename__ = "home_categories_order"
    id = Column(Integer, primary_key=True)
    order = Column(Integer, unique=True)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    category = relationship("Category", backref="home_categories_order")

    def __init__(self, order, category_id):
        self.order = order
        self.category_id = category_id
        session.add(self)
        session.commit()


if __name__ == "__main__":
    try:
        remove("database.db")
    except FileNotFoundError:
        pass

Base.metadata.create_all(engine)
    # engine.dispose()
