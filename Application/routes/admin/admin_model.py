from flask_admin.model.template import macro
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import fields
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from sqlalchemy import func
from Application.database import model as db
from Application.utils.handle_files import *
Session = db.session
from flask import url_for,flash

class ShopView(ModelView):
    can_delete = False
    form_excluded_columns = ["products"]
    list_template = "admin/shop.html"
    column_searchable_list = [
        "vendor_name", 
        "shop_name", 
        "date_of_registration", 
        "user_name", 
        "address", 
        "email",
        "contact"
        ]
    column_filters = ["date_of_registration"]
    column_details_exclude_list = ["password"]
    column_exclude_list = ["password"]
    can_view_details = True
    can_export = True
    form_overrides = {
        "additional_file_names":fields.FileField,
        "vendor_pic_file_name": fields.FileField
    }
    column_formatters = {
        "additional_file_names":macro("render_vendor_file"),
        "vendor_pic_file_name": macro("render_picture")
    }
    form_excluded_columns = ["product"]

    def create_model(self, form):
        picture = save_picture(
            form.vendor_pic_file_name.data,
            "static/profile_pics",
            800,800
            )
        document = save_document(form.additional_file_names.data)
        db.Shop(
            form.vendor_name.data, 
            picture, 
            form.user_name.data,
            form.password.data,
            form.address.data,
            form.email.data,
            form.contact.data,
            form.shop_name.data,
            form.company_name.data,
            form.location.data,
            form.description.data,
            form.tin_number.data,
            form.license_number.data,
            document,
            form.second_contact.data
        )
        flash("created successfully", "success")
    
    def update_model(self, form, model):
        update = Session.query(
            db.Shop
        ).filter(
            db.Shop.id == model.id
        ).update(
            {
                "vendor_name": form.vendor_name.data, 
                "user_name": form.user_name.data,
                "address": form.address.data,
                "email": form.email.data,
                "contact": form.contact.data,
                "shop_name": form.shop_name.data,
                "company_name": form.company_name.data,
                "location": form.location.data,
                "description": form.description.data,
                "tin_number": form.tin_number.data,
                "license_number": form.license_number.data,
                "second_contact": form.second_contact.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False


class ProductView(ModelView):
    can_delete = False
    can_view_details = True
    can_export = True
    can_set_page_size = True
    column_list = (
        "name", 
        "sub_category.name",
        "shop.shop_name"
        )
    column_labels = {
        "name": "Name",
        "sub_category.name": "Sub Category",
        "shop.shop_name": "Shop Name"

    }
    form_excluded_columns = ("product_details","trackproducts")
    column_searchable_list = [
        "name",
        "shop.shop_name"
    ]

    def scaffold_form(self):
        form_class = super(ProductView, self).scaffold_form()
        form_class.sub_category = fields.SelectField(
            label="Sub Category",
            coerce=int,
            choices=Session.query(
                db.SubCategory.sub_category_id, 
                db.SubCategory.name
                ).all()
        )
        form_class.shop = fields.SelectField(
            label="Shop",
            coerce=int,
            choices=Session.query(
                db.Shop.id, 
                db.Shop.shop_name
                ).all()
        )
        return form_class

    def create_model(self, form):
        sub_category = db.SubCategory.read_sub_category(
            db.SubCategory, 
            form.sub_category.data
            )
        shop = db.Shop.read_vendor(
            db.Shop, 
            form.shop.data
            )
        db.Product(form.name.data,sub_category,shop)
        flash("Record was successfully created", "success")
     
    def update_model(self, form, model):
        update = Session.query(
            db.Product
        ).filter(
            db.Product.product_id == model.product_id
        ).update(
            {
                "name":form.name.data,
                "sub_category_id":form.sub_category.data,
                "shop_id": form.shop.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False

class ProductDetailsView(ModelView):
    can_view_details = True
    can_export = True
    can_delete = False
    list_template = "admin/product_details.html"
    column_list = (
        "product_type", 
        "brand",
        "color",
        "size",
        "front_picture",
        "back_picture",
        "key_features",
        "quantity",
        "prize",
        "weight",
        "description",
        "warranty",
        "guarantee",
        "promotional_price",
        "product.name", 
        "product.sub_category.name"
        )
    column_labels = {
        "product.name": "Product Name", 
        "product.sub_category.name": "Sub Category Name"
    }
    form_overrides = {
        "front_picture":fields.FileField,
        "back_picture": fields.FileField,
        "weight": fields.StringField
    }
    form_excluded_columns = ["sales", "stock_details", "order","stock"]
    column_formatters = {
        "front_picture":macro("render_front_picture"),
        "back_picture":macro("render_back_picture")
    }
    column_searchable_list = [
        "product.name",
        "product.sub_category.name",
        "brand"
    ]

    def scaffold_form(self):
        form_class = super(ProductDetailsView, self).scaffold_form()
        form_class.product = fields.SelectField(
            label="Product",
            coerce=int,
            choices=Session.query(
                db.Product.product_id, 
                db.Product.name
                ).all()
        )
        return form_class

    def create_model(self, form):
        product = db.Product.read_product(db.Product, form.product.data)
        front_pic = save_picture(
            form.front_picture.data,
            "static/vendor_product_pictures",
            800,800
            )
        back_pic = save_picture(
            form.back_picture.data,
            "static/vendor_product_pictures",
            800,800
            )
        db.ProductDetails(
            form.product_type.data,
            form.brand.data,
            form.color.data,
            form.size.data,
            front_pic,
            back_pic,
            form.key_features.data,
            form.quantity.data,
            form.prize.data,
            form.weight.data,
            form.description.data,
            form.warranty.data,
            form.guarantee.data,
            product
        )
        flash("Record was successfully created", "success")
     
    def update_model(self, form, model):
        update = Session.query(
            db.ProductDetails
        ).filter(
            db.ProductDetails.prod_details_id == model.prod_details_id
        ).update(
            {
                "product_type": form.product_type.data,
                "brand": form.brand.data,
                "color": form.color.data,
                "size": form.size.data,
                "key_features": form.key_features.data,
                "quantity": form.quantity.data,
                "prize": form.prize.data,
                "weight": form.weight.data,
                "description": form.description.data,
                "warranty": form.warranty.data,
                "guarantee": form.guarantee.data,
                "product_id": form.product.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False

class CategoryView(ModelView):
    can_delete = False
    form_excluded_columns = ["sub_category","home_categories_order"]
    column_searchable_list = [
        "name"
    ]

class SubCategoryView(ModelView):
    can_delete = False
    column_list = ("name", "category.name")
    column_labels = {
        "name": "Name",
        "category.name": "Category"

    }
    form_excluded_columns = ["product"]
    column_searchable_list = [
        "name"
    ]

    def scaffold_form(self):
        form_class = super(SubCategoryView, self).scaffold_form()
        form_class.category = fields.SelectField(
            label="Category",
            coerce=int,
            choices=Session.query(
                db.Category.category_id, 
                db.Category.name
                ).all()
        )
        return form_class

    def create_model(self, form):
        cat = db.Category.read_category(db.Category, form.category.data)
        db.SubCategory(form.name.data, cat)
        flash("Record was successfully created", "success")
     
    def update_model(self, form, model):
        update = Session.query(
            db.SubCategory
        ).filter(
            db.SubCategory.sub_category_id == model.sub_category_id
        ).update(
            {
                "name":form.name.data,
                "category_id":form.category.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False

    form_ajax_refs = {
        "category": QueryAjaxModelLoader(
            "category", 
            Session, 
            db.Category,
            fields=["name"] 
        )
    }

class BrandView(ModelView):
    can_delete = False
    column_searchable_list = [
        "name"
    ]
class CustomerView(ModelView):
    form_excluded_columns = ["order"]
    column_filters = ["country", "date_of_registration"]
    can_create = False
    can_view_details = True
    can_export = True
    can_delete = False

class AdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        customer_number = Session.query(func.count(db.Customer.id)).scalar()
        shops_number = Session.query(func.count(db.Shop.id)).scalar()
        sales_amount = Session.query(func.sum(db.Sales.amount)).scalar()
        distinct_products = Session.query(func.count(db.Product.product_id)).scalar()
        products_available = Session.query(
            func.sum(db.ProductDetails.quantity)
            ).scalar()
        products_sold = Session.query(func.sum(db.Sales.quantity)).scalar()

        if products_available is None:
            products_available = 0

        if products_sold is None:
            products_sold = 0

        if sales_amount is None:
            sales_amount = 0

        products_number = products_available + products_sold

        return self.render(
            "admin/index.html", 
            customer_number=customer_number,
            shops_number=shops_number,
            products_number=products_number,
            sales_amount=sales_amount,
            products_available=products_available,
            products_sold=products_sold,
            distinct_products=distinct_products
            )

class HomeSlideShowImagesView(ModelView):
    list_template = "admin/home_slide_show_settings.html"
    form_overrides = {
        "order": fields.IntegerField,
        "image_name": fields.FileField
    }
    column_formatters = {
        "image_name":macro("render_image")
    }
    
    def create_model(self, form):
        picture = save_picture(
            form.image_name.data,
            "static/vendor_product_pictures",
            800,800
            )
        db.HomeSlideShowImages(form.order.data,picture,form.caption.data)
        flash("Record was successfully created", "success")
    def update_model(self, form, model):
        picture = save_picture(
            form.image_name.data,
            "static/vendor_product_pictures",
            800,800
            )
        update = Session.query(
            db.HomeSlideShowImages
        ).filter(
            db.HomeSlideShowImages.image_id == model.id
        ).update(
            {
                "order":int(form.order.data),
                "image_name":picture,
                "caption": form.caption.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False
        

class HomeCategoriesOrderView(ModelView):
    column_list = ("order", "category.name")
    column_labels = {
        "category.name": "Name"
    }

    def scaffold_form(self):
        form_class = super(HomeCategoriesOrderView, self).scaffold_form()
        form_class.category = fields.SelectField(
            label="Category",
            coerce=int,
            choices=Session.query(
                db.Category.category_id, db.Category.name
                ).all()
        )
        return form_class

    def create_model(self, form):
        db.HomeCategoriesOrder(int(form.order.data),form.category.data)
        flash("Record was successfully created", "success")
    
    def update_model(self, form, model):
        update = Session.query(
            db.HomeCategoriesOrder
        ).filter(
            db.HomeCategoriesOrder.id == model.id
        ).update(
            {
                "order":int(form.order.data),
                "category_id":form.category.data
            })
        if update:
            Session.commit()
            return True
        else:
            return False
    