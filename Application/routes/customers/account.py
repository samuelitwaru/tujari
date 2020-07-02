from flask import render_template, redirect, Blueprint, request, url_for, flash, abort, session as period
from .forms import UpdateCustomerForm, UpdatePasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from Application.database.model import session


account=Blueprint('account', __name__)

@account.route('/update-account', methods=["POST", "GET"])
@login_required
def update_account():
    customer = current_user
    form = UpdateCustomerForm(obj=customer)
    password_form = UpdatePasswordForm()

    if form.validate_on_submit():
        # update account details
        customer.name = form.name.data
        customer.email = form.email.data
        customer.contact = form.contact.data
        customer.country = form.country.data
        customer.city = form.city.data
        session.commit()
        flash('Updated account.', 'success')
        return redirect(url_for('account.update_account'))
    else:
        tab='personal'
        return render_template('customer/account.html', form=form, password_form=password_form, current_tab=tab)


@account.route('/update-password', methods=["POST", "GET"])
@login_required
def update_password():
    customer = current_user
    form = UpdateCustomerForm(obj=customer)
    password_form = UpdatePasswordForm()
    if password_form.validate_on_submit():
        customer.hash_password(password_form.new.data)
        session.commit()
        flash('Updated password.', 'success')
        return redirect(url_for('account.update_password'))
    else:
        tab = 'password'
        return render_template('customer/account.html', form=form, password_form=password_form, current_tab=tab)