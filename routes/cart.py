
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Product, CartItem

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.get("/")
@login_required
def view():
    items = CartItem.query.filter_by(user_id=current_user.id).all()

    subtotal = sum(
        item.product.final_price * item.quantity for item in items
    )

    savings = sum(
        (item.product.price - item.product.final_price) * item.quantity
        for item in items
    )

    return render_template(
        "cart.html",
        items=items,
        subtotal=round(subtotal, 2),
        savings=round(savings, 2)
    )


@cart_bp.post("/add/<int:product_id>")
@login_required
def add(product_id):
    product = Product.query.get_or_404(product_id)

    quantity = request.form.get("quantity", 1, type=int)
    size = request.form.get(
        "size",
        product.size_list[0] if product.size_list else "Free Size"
    ).strip()

    if product.stock < 1:
        flash("This product is out of stock.", "danger")
    elif quantity is None or quantity < 1 or quantity > 10:
        flash("Choose a quantity between 1 and 10.", "danger")
    elif size not in product.size_list:
        flash("Please select a valid size.", "danger")
    else:
        item = CartItem.query.filter_by(
            user_id=current_user.id,
            product_id=product.id,
            selected_size=size
        ).first()

        if item:
            item.quantity = min(
                item.quantity + quantity,
                product.stock,
                10
            )
        else:
            db.session.add(
                CartItem(
                    user_id=current_user.id,
                    product_id=product.id,
                    quantity=min(quantity, product.stock),
                    selected_size=size
                )
            )

        product.popularity += 1
        db.session.commit()
        flash("Product added to your cart.", "success")

    return redirect(
        request.referrer or url_for("products.detail", product_id=product_id)
    )


@cart_bp.post("/update/<int:item_id>")
@login_required
def update(item_id):
    item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()

    quantity = request.form.get("quantity", type=int)

    if (
        quantity is None or quantity < 1 or
        quantity > min(10, item.product.stock)
    ):
        flash("Enter a valid quantity within the available stock.", "danger")
    else:
        item.quantity = quantity
        db.session.commit()
        flash("Cart updated successfully.", "success")

    return redirect(url_for("cart.view"))


@cart_bp.post("/remove/<int:item_id>")
@login_required
def remove(item_id):
    item = CartItem.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    flash("Product removed from your cart.", "info")
    return redirect(url_for("cart.view"))
