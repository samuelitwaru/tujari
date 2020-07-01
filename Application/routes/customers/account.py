from flask import render_template, redirect, Blueprint, request, url_for, flash, abort, session as period
from .forms import UpdateCustomerForm, UpdatePasswordForm, AddressForm
from flask_login import current_user, login_user, logout_user, login_required


account=Blueprint('account', __name__)

@account.route('/update-account', methods=["POST", "GET"])
@login_required
def update_account():
    customer = current_user
    form = UpdateCustomerForm(obj=customer)
    password_form = UpdatePasswordForm()
    address_form = AddressForm()

    if form.validate_on_submit():
        # get POST args
        pass
        # update account details

    return render_template('customer/account.html', form=form, password_form=password_form, address_form=address_form)



@account.route('/update-password', methods=["POST"])
@login_required
def update_password():
    customer = current_user
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        # get POST args
        pass
        # update account password
    
    return redirect(url_for('acccount.update_account'))


@account.route('/update-password', methods=["POST"])
@login_required
def update_address():
    customer = current_user
    address = Customer.address
    form = AddressForm()

    if form.validate_on_submit():
        # get POST args
        pass
        # update account password
    
    return redirect(url_for('acccount.update_account'))
