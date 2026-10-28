
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship(
        "CartItem", backref="user", cascade="all, delete-orphan"
    )
    wishlist_items = db.relationship(
        "WishlistItem", backref="user", cascade="all, delete-orphan"
    )
    orders = db.relationship(
        "Order", backref="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Store a secure hash instead of the original password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against its stored hash."""
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False, default="Eesha's Choice")
    category = db.Column(db.String(50), nullable=False, index=True)
    subcategory = db.Column(db.String(80), nullable=False, default="General")
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0, nullable=False)
    sizes = db.Column(db.String(200), default="Free Size")
    colour = db.Column(db.String(50), default="Multicolour")
    style_tag = db.Column(db.String(50), default="casual")
    occasion = db.Column(db.String(80), default="Everyday")
    image = db.Column(db.String(500), default="")
    rating = db.Column(db.Float, default=4.0)
    stock = db.Column(db.Integer, default=10, nullable=False)
    popularity = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship("CartItem", backref="product")
    wishlist_items = db.relationship("WishlistItem", backref="product")

    @property
    def final_price(self):
        """Calculate the selling price after discount."""
        return round(self.price * (1 - self.discount / 100), 2)

    @property
    def size_list(self):
        """Convert comma-separated sizes into a Python list."""
        return [size.strip() for size in (self.sizes or "").split(",") if size.strip()]


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    quantity = db.Column(db.Integer, default=1, nullable=False)
    selected_size = db.Column(db.String(30), default="Free Size")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", "selected_size"),
    )


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id"),
    )


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(15), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    payment_method = db.Column(
        db.String(30), default="Cash on Delivery", nullable=False
    )
    status = db.Column(db.String(30), default="Placed", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        "OrderItem", backref="order", cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=True
    )
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    selected_size = db.Column(db.String(30), default="Free Size")
