from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from Application import app
from Application.database import model as db
from .admin_model import *
import os.path as po

path  = po.join(po.dirname(app.root_path),"Application/static/vendor_documents")
Session = db.session

admin = Admin(app,"", template_mode="bootstrap3", index_view=AdminHomeView())
admin.add_view(ShopView(db.Shop, Session))
admin.add_view(FileAdmin(path, name="Vendor Documents" ))
admin.add_view(CustomerView(db.Customer, Session))
admin.add_view(CategoryView(db.Category, Session, category="Product Categories"))
admin.add_view(SubCategoryView(db.SubCategory, Session, category="Product Categories"))
admin.add_view(BrandView(db.Brand, Session))
admin.add_view(ProductView(db.Product, Session, category="Products"))
admin.add_view(ProductDetailsView(db.ProductDetails, Session, category="Products"))
admin.add_view(ModelView(db.Order, Session))


admin.add_view(ModelView(db.Payment, Session, category="Payments"))
admin.add_sub_category("Payment Methods","Payments")

admin.add_view(ModelView(db.MobileMoney, Session, category="Payment Methods"))
admin.add_view(ModelView(db.Visa, Session, category="Payment Methods"))
admin.add_view(ModelView(db.CashOnDelivery, Session, category="Payment Methods"))

admin.add_view(ModelView(db.Delivery, Session, category="Deliveries"))
admin.add_view(ModelView(db.DeliveryDetails, Session, category="Deliveries"))

admin.add_view(ModelView(db.Stock, Session, category="Stock&Sales Tracking"))
admin.add_view(ModelView(db.Sales, Session, category="Stock&Sales Tracking"))
admin.add_view(HomeSlideShowImagesView(db.HomeSlideShowImages, Session, category="Home Page Settings"))
admin.add_view(HomeCategoriesOrderView(db.HomeCategoriesOrder, Session, category="Home Page Settings"))