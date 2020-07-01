"""empty message

Revision ID: eb90a4e463e0
Revises: 
Create Date: 2020-06-05 16:38:04.468130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb90a4e463e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('brand_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('picture_file_name', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('date_of_registration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('customer_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('_zip', sa.String(), nullable=True),
    sa.Column('district', sa.String(), nullable=True),
    sa.Column('street', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('delivery',
    sa.Column('delivery_id', sa.Integer(), nullable=False),
    sa.Column('deliverer_name', sa.Integer(), nullable=True),
    sa.Column('driver_license_number', sa.String(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('carrier_means', sa.String(), nullable=True),
    sa.Column('carrier_type', sa.String(), nullable=True),
    sa.Column('carrier_license_plate_number', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('delivery_id')
    )
    op.create_table('shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vendor_name', sa.String(), nullable=True),
    sa.Column('vendor_pic_file_name', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('shop_name', sa.String(), nullable=True),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date_of_registration', sa.DateTime(), nullable=True),
    sa.Column('tin_number', sa.String(), nullable=True),
    sa.Column('license_number', sa.String(), nullable=True),
    sa.Column('additional_file_names', sa.String(), nullable=True),
    sa.Column('second_contact', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('second_contact')
    )
    op.create_index(op.f('ix_shop_user_name'), 'shop', ['user_name'], unique=True)
    op.create_table('addtocart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_image', sa.String(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('weight', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sub_category',
    sa.Column('sub_category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.category_id'], ),
    sa.PrimaryKeyConstraint('sub_category_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('sub_category_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shop.id'], ),
    sa.ForeignKeyConstraint(['sub_category_id'], ['sub_category.sub_category_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('product_details',
    sa.Column('prod_details_id', sa.Integer(), nullable=False),
    sa.Column('product_type', sa.String(), nullable=True),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('front_picture', sa.String(), nullable=True),
    sa.Column('back_picture', sa.String(), nullable=True),
    sa.Column('key_features', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('prize', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('warranty', sa.String(), nullable=True),
    sa.Column('guarantee', sa.String(), nullable=True),
    sa.Column('promotional_price', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.PrimaryKeyConstraint('prod_details_id')
    )
    op.create_table('trackproducts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('product_details_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['product_details_id'], ['product_details.prod_details_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('sales',
    sa.Column('sales_id', sa.Integer(), nullable=False),
    sa.Column('product_details_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_details_id'], ['product_details.prod_details_id'], ),
    sa.PrimaryKeyConstraint('sales_id')
    )
    op.create_table('stock',
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('product_details_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_details_id'], ['product_details.prod_details_id'], ),
    sa.PrimaryKeyConstraint('stock_id')
    )
    op.create_table('delivery_details',
    sa.Column('delivery_details_id', sa.Integer(), nullable=False),
    sa.Column('delivery_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('delivery_address', sa.String(), nullable=True),
    sa.Column('delivery_ref_number', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['delivery_id'], ['delivery.delivery_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('delivery_details_id')
    )
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('payment_date', sa.DateTime(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    op.create_table('cash_on_delivery',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('transaction_ref', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.payment_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_table('mobile_money',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('transaction_ref', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.payment_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_table('visa',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('contact', sa.String(), nullable=True),
    sa.Column('account_number', sa.String(), nullable=True),
    sa.Column('security_number', sa.Integer(), nullable=True),
    sa.Column('expiry_date', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('transaction_ref', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payment.payment_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visa')
    op.drop_table('mobile_money')
    op.drop_table('cash_on_delivery')
    op.drop_table('payment')
    op.drop_table('delivery_details')
    op.drop_table('stock')
    op.drop_table('sales')
    op.drop_table('order')
    op.drop_table('trackproducts')
    op.drop_table('product_details')
    op.drop_table('product')
    op.drop_table('sub_category')
    op.drop_table('addtocart')
    op.drop_index(op.f('ix_shop_user_name'), table_name='shop')
    op.drop_table('shop')
    op.drop_table('delivery')
    op.drop_table('customer_address')
    op.drop_table('customer')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###