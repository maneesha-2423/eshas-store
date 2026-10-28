
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, abort
)
from flask_login import login_required, current_user
from models import db, Product

products_bp = Blueprint("products", __name__)

CATEGORIES = ["Men", "Women", "Boys", "Girls", "Kids", "Jewellery"]


@products_bp.get("/shop")
def shop():
    return _render_products()


@products_bp.get("/category/<category>")
def category(category):
    if category not in CATEGORIES:
        abort(404)

    return _render_products(category=category)


def _render_products(category=None):
    query = Product.query

    selected_category = category or request.args.get("category", "").strip()

    if selected_category in CATEGORIES:
        query = query.filter(Product.category == selected_category)

    keyword = request.args.get("q", "").strip()

    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            db.or_(
                Product.name.ilike(search),
                Product.brand.ilike(search),
                Product.category.ilike(search),
                Product.subcategory.ilike(search)
            )
        )

    subcategory = request.args.get("subcategory", "").strip()
    if subcategory:
        query = query.filter(Product.subcategory == subcategory)

    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()

    try:
        if min_price:
            query = query.filter(
                Product.price * (1 - Product.discount / 100)
                >= float(min_price)
            )
    except ValueError:
        min_price = ""

    try:
        if max_price:
            query = query.filter(
                Product.price * (1 - Product.discount / 100)
                <= float(max_price)
            )
    except ValueError:
        max_price = ""

    size = request.args.get("size", "").strip()
    if size:
        query = query.filter(Product.sizes.ilike(f"%{size}%"))

    brand = request.args.get("brand", "").strip()
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    rating = request.args.get("rating", "").strip()
    try:
        if rating:
            query = query.filter(Product.rating >= float(rating))
    except ValueError:
        rating = ""

    sort = request.args.get("sort", "popular")

    if sort == "price_asc":
        query = query.order_by(
            (Product.price * (1 - Product.discount / 100)).asc()
        )
    elif sort == "price_desc":
        query = query.order_by(
            (Product.price * (1 - Product.discount / 100)).desc()
        )
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(
            Product.popularity.desc(),
            Product.rating.desc()
        )

    products = query.all()

    brands = [
        item[0] for item in
        db.session.query(Product.brand).distinct().order_by(Product.brand).all()
    ]

    subcategories = [
        item[0] for item in
        db.session.query(Product.subcategory)
        .distinct().order_by(Product.subcategory).all()
    ]

    return render_template(
        "home.html",
        products=products,
        categories=CATEGORIES,
        selected_category=selected_category,
        keyword=keyword,
        sort=sort,
        brands=brands,
        subcategories=subcategories,
        filters={
            "min_price": min_price,
            "max_price": max_price,
            "size": size,
            "brand": brand,
            "rating": rating,
            "subcategory": subcategory
        }
    )


@products_bp.get("/product/<int:product_id>")
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)


@products_bp.route("/admin/products", methods=["GET", "POST"])
@login_required
def admin_products():
    if not current_user.is_admin:
        abort(403)

    if request.method == "POST":
        action = request.form.get("action", "create")
        product_id = request.form.get("product_id", type=int)

        product = (
            db.session.get(Product, product_id)
            if product_id else None
        )

        if action == "delete":
            if product:
                db.session.delete(product)
                db.session.commit()
                flash("Product deleted successfully.", "success")
            return redirect(url_for("products.admin_products"))

        if action == "edit" and product is None:
            flash("Product not found.", "danger")
            return redirect(url_for("products.admin_products"))

        try:
            name = request.form.get("name", "").strip()
            price = float(request.form.get("price", "0"))
            discount = int(request.form.get("discount", "0"))
            stock = int(request.form.get("stock", "0"))
            category_value = request.form.get("category", "Women")

            if (
                not name or price <= 0 or
                not 0 <= discount <= 90 or stock < 0 or
                category_value not in CATEGORIES
            ):
                raise ValueError

            if product is None:
                product = Product()
                db.session.add(product)

            product.name = name
            product.brand = request.form.get(
                "brand", "Eesha Select"
            ).strip() or "Eesha Select"
            product.category = category_value
            product.subcategory = request.form.get(
                "subcategory", "Other"
            ).strip() or "Other"
            product.price = price
            product.discount = discount
            product.stock = stock
            product.sizes = request.form.get(
                "sizes", "Free Size"
            ).strip() or "Free Size"
            product.colour = request.form.get(
                "colour", "Multicolour"
            ).strip() or "Multicolour"
            product.style_tag = request.form.get(
                "style_tag", "casual"
            ).strip() or "casual"
            product.occasion = request.form.get(
                "occasion", "everyday"
            ).strip() or "everyday"
            product.image = request.form.get("image", "").strip()
            product.description = request.form.get(
                "description", ""
            ).strip()

            db.session.commit()
            flash("Product saved successfully.", "success")
            return redirect(url_for("products.admin_products"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash(
                "Please check the product name, price, discount, stock and category.",
                "danger"
            )

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        "admin_products.html",
        products=products,
        categories=CATEGORIES
    )
