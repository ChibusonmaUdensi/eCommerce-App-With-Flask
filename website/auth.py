from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, ChangePasswordForm
from .models import  Customer
from . import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_


auth= Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST', 'GET'])

def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password1 = form.password1.data
        password2 = form.password2.data
        # username = form.username.data

        if password1 == password2:
            new_customer = Customer(
            firstname=first_name,
            lastname=last_name,
            email=email,
            )
            new_customer.password = password1  # This sets the password_hash

            try:
                db.session.add(new_customer)
                db.session.commit()
            
                flash('You are now registered and can log in')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account not created! Email already exists')

            form.first_name.data= ''
            form.last_name.data= ''
            form.email.data= ''
            # form.username.data= ''
            form.password1.data= ''
            form.password2.data= ''

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                flash('You are now logged in')
                return redirect('/')
            else:
                flash('Login Unsuccessful. Please check password')
        else:
            flash('Account doesn.t exist!. Please Sign Up')

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['POST', 'GET'])
@login_required

def logout():
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
   customer = Customer.query.get(customer_id)
   print('Customer ID:', customer_id)
   return render_template('profile.html', customer=customer)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = ChangePasswordForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Password Updated Successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New Passwords do not match!!')

        else:
            flash('Current Password is Incorrect')
    return render_template('change_password.html', form=form)