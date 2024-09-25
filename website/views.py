from flask import Blueprint, render_template, flash, redirect, jsonify, request
from . import db 
from flask_login import login_user, login_required, logout_user, current_user
from .models import Product, Cart
from . import db
views = Blueprint('views', __name__)


API_PUBLISHABLE_KEY ='atsk_244049a65b60f0e83350956d9d0ff096df774f3ad5b0b2548713f7f4f97e8489d7369c7b'


@views.route('/')
def home():

    items= Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                            if current_user.is_authenticated else [])

@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    
    if item_exists:
        try:
            item_exists.quantity += 1
            db.session.commit()
            flash(f'Quantity of {item_exists.product.product_name} has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of { item_exists.product.product_name } not updated')
            return redirect(request.referrer)
    

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} has been added to your cart')
        return redirect(request.referrer)
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'Item {new_cart_item.product.product_name} not added to cart')
        return redirect(request.referrer)
    
@views.route('/cart')
@login_required
def show_cart():
      cart = Cart.query.filter_by(customer_link=current_user.id).all() 
      amount = 0
      for item in cart:
          amount += item.product.current_price * item.quantity

      return render_template('cart.html', cart=cart, amount=amount, total = amount + 200)


@views.route('/pluscart/')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity
        


        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    

    
@views.route('/minuscart/')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity
        


        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)
    
@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()


        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity
        


        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200
        }

        return jsonify(data)