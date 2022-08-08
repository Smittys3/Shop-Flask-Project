from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import User, db, Merch

shop = Blueprint('shop', __name__, template_folder='shoptemplates')

@shop.route('/shop', methods=["GET", "POST"])
@login_required
def goShop():
    merch = Merch.query.all()
    return render_template('shop.html', merch=merch)

@shop.route('/cart', methods=["GET", "POST"])
@login_required
def goCart():
    user = User.query.get(current_user.id)
    cart = user.cart.all()
    total = len(cart)
    return render_template('cart.html', cart=cart, user=user, total=total)

@shop.route('/add/<string:name>')
@login_required
#add a singler item to cart
def addCart(name):
    merch = Merch.query.filter_by(name=name).first()
    current_user.cart.append(merch)
    db.session.commit()
    flash('Item added to cart.', 'success')
    return redirect(url_for('shop.goShop'))

@shop.route('/remove/<string:name>')
@login_required
#removes a single item form cart
def removeCart(name):
    merch = Merch.query.filter_by(name=name).first()
    current_user.cart.remove(merch)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    return redirect(url_for('shop.goCart'))


@shop.route('/removeall')
@login_required
def removeall():
    merch = Merch.query.all()
    for m in merch:
        if m in current_user.cart:
            current_user.cart.remove(m)
            db.session.commit()
    flash('All Items Removed!', 'success')
    return redirect(url_for('shop.goCart'))
