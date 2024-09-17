from flask import Blueprint, render_template, send_from_directory, flash, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
admin= Blueprint('admin', __name__)
from .models import Product
from . import db

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 6:
        form = ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name = secure_filename(file.filename)  
            # secure_filename returns sanitized version of our file name ie it removes white spaces and invalid characters from the file names

            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_shop_item =Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale

            new_shop_item.product_picture = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added successfully')
                print('Product Added')
                return render_template('add-shop-items.html', form=form)
            except Exception as e:
                print(e)
                flash('Failed to add product')
            

        return render_template('add-shop-items.html', form=form)
    return render_template('404.html')

@admin.route('/shop-items',methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 6:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')

@admin.route('/update-item/<int:item_id>', methods=['GET','POST'])
@login_required
def update_item(item_id):
    if current_user.id == 6:
        item_to_update = Product.query.get(item_id)
        form = ShopItemsForm()
      
        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name = secure_filename(file.filename)
            filepath = f'./media/{file_name}'

            file.save(filepath)
            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                product_picture=filepath))
                db.session.commit()
                flash(f'{product_name} updated successfully')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Updated')
                flash(f'Item not Updated!!1')
        return render_template('update_item.html', form=form) 
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 6:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash(f'{item_to_delete.product_name} deleted successfully')
            return redirect('/shop-items')
        except Exception as e:
            print('Product not deleted', e)
            flash(f'Item not deleted!!')
        return redirect('/shop-items')
    return render_template('404.html')
