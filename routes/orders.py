
import re

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, CartItem, Order, OrderItem

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items = CartItem.query.filter_by(
        user_id=current_user.id
    ).all()

    if not items:
        flash("Your cart is empty.", "info")
        return redirect(url_for("cart.view"))

    total = round(
        sum(item.product.final_price * item.quantity for item in items),
        2
    )

    if request.method == "POST":
        full_name = request.form.get(
            "full_name", request.form.get("name", "")
        ).strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        postal_code = request.form.get(
            "postal_code", request.form.get("pincode", "")
        ).strip()
        payment_method = request.form.get(
            "payment_method", "COD"
        ).strip()

        if not all([
            full_name, phone, address, city, state, postal_code
        ]):
            flash("Please fill in all delivery details.", "danger")

        elif not re.fullmatch(r"[0-9+()\-\s]{10,16}", phone):
            flash("Please enter a valid phone number.", "danger")

        elif not re.fullmatch(r"\d{6}", postal_code):
            flash("Please enter a valid 6-digit PIN code.", "danger")

        elif payment_method not in ["COD"]:
            flash("Please select a supported payment method.", "danger")

        elif any(
            item.product.stock < item.quantity for item in items
        ):
            flash(
                "Some products no longer have enough stock. Please update your cart.",
                "danger"
            )
            return redirect(url_for("cart.view"))

        else:
            order = Order(
                user_id=current_user.id,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                total_amount=total,
                payment_method=payment_method,
                status="Placed"
            )

            db.session.add(order)
            db.session.flush()

            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    product_name=item.product.name,
                    price=item.product.final_price,
                    quantity=item.quantity,
                    selected_size=item.selected_size
                )

                db.session.add(order_item)
                item.product.stock -= item.quantity
                db.session.delete(item)

            db.session.commit()

            flash(
                f"Order #{order.id} placed successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "orders.confirmation",
                    order_id=order.id
                )
            )

    return render_template(
        "checkout.html",
        items=items,
        total=total
    )


@orders_bp.get("/order-confirmation/<int:order_id>")
@login_required
def confirmation(order_id):
    order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "order_confirmation.html",
        order=order
    )


@orders_bp.get("/orders")
@login_required
def history():
    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(Order.created_at.desc()).all()

    return render_template(
        "orders.html",
        orders=orders
    )
