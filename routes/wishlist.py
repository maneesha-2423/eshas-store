
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Product, WishlistItem

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/wishlist")


@wishlist_bp.get("/")
@login_required
def view():
    items = WishlistItem.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template("wishlist.html", items=items)


@wishlist_bp.post("/toggle/<int:product_id>")
@login_required
def toggle(product_id):
    product = Product.query.get_or_404(product_id)

    item = WishlistItem.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()

    if item:
        db.session.delete(item)
        flash("Product removed from your wishlist.", "info")
    else:
        db.session.add(
            WishlistItem(
                user_id=current_user.id,
                product_id=product.id
            )
        )
        flash("Product added to your wishlist.", "success")

    db.session.commit()

    return redirect(request.referrer or url_for("wishlist.view"))


@wishlist_bp.post("/remove/<int:item_id>")
@login_required
def remove(item_id):
    item = WishlistItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    flash("Product removed from your wishlist.", "info")
    return redirect(url_for("wishlist.view"))
