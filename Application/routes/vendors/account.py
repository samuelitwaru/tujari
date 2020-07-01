from flask import render_template, redirect, Blueprint, request, url_for, flash, abort, send_file
from .forms import UpdateVendorBusinessForm, UpdateVendorForm, UpdatePasswordForm, UpdateVendorImageForm, UpdateVendorFileForm
from flask_login import current_user, login_user, logout_user, login_required
from Application.utils.handle_files import *
import os
from Application import app
from Application.database.model import session

vendor_account=Blueprint('vendor_account', __name__)

@vendor_account.route('/update-vendor', methods=["POST", "GET"])
@login_required
def update_vendor():
    vendor = current_user
    form = UpdateVendorForm(obj=vendor)
    password_form = UpdatePasswordForm()
    business_form = UpdateVendorBusinessForm(obj=vendor)
    profile_form = UpdateVendorImageForm(obj=vendor)
    file_form = UpdateVendorFileForm(obj=vendor)

    if form.validate_on_submit():
        # update account details
        vendor.vendor_name = form.vendor_name.data
        vendor.address = form.address.data
        vendor.email = form.email.data
        vendor.contact = form.contact.data

        session.commit()
    return render_template('vendor/account.html', form=form, password_form=password_form, business_form=business_form, profile_form=profile_form, file_form=file_form)


@vendor_account.route('/update-profile-picture', methods=["POST", "GET"])
@login_required
def update_profile_picture():
	vendor = current_user
	form = UpdateVendorImageForm()
	if form.validate_on_submit():
		# get params
		new_picture = form.vendor_pic_file_name.data
		# delete current picture
		current_path = app.config.get('BASE_DIR') + url_for('static', filename=f'profile_pics/{vendor.vendor_pic_file_name}')
		try:
			os.remove(current_path)
		except FileNotFoundError:
			pass
		# update profile picture
		profile_pic = save_picture(new_picture, 'static/profile_pics', 125,125)
		vendor.vendor_pic_file_name = profile_pic
		session.commit()
	return redirect(url_for('vendor_account.update_vendor'))


@vendor_account.route('/update-vendor-business', methods=["POST", "GET"])
@login_required
def update_vendor_business():
    vendor = current_user
    form = UpdateVendorBusinessForm(obj=vendor)

    if form.validate_on_submit():
        # update account details
        vendor.shop_name = form.shop_name.data
        vendor.company_name = form.company_name.data
        vendor.location = form.location.data
        vendor.description = form.description.data
        vendor.tin_number = form.tin_number.data
        vendor.license_number = form.license_number.data
        
        session.commit()
    return redirect(url_for('vendor_account.update_vendor'))



@vendor_account.route('/update-vendor-file', methods=["POST", "GET"])
@login_required
def update_vendor_file():
	vendor = current_user
	form = UpdateVendorFileForm(obj=vendor)
	if form.validate_on_submit():
		new_doc = form.additional_file_names.data

		# delete current doc
		current_path = app.config.get('BASE_DIR') + url_for('static', filename=f'vendor_documents/{vendor.additional_file_names}')
		try:
			os.remove(current_path)
		except FileNotFoundError:
			pass
		# update doc
		doc_name = save_document(new_doc)
		vendor.additional_file_names = doc_name
		print(">>>>>>>>>>>>>>>>>>>>", vendor.additional_file_names)
		session.commit()
	return redirect(url_for('vendor_account.update_vendor'))


@vendor_account.route('/read-vendor-file')
@login_required
def read_vendor_file():
	vendor = current_user
	print(">>>>>>>>>>>>>>>>>>>>", vendor.additional_file_names)
	return send_file(app.config.get('BASE_DIR') + url_for('static', filename=f'vendor_documents/{vendor.additional_file_names}'))