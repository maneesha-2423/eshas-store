
from flask import Flask, render_template
from flask_login import LoginManager, current_user

from config import Config
from models import db, User, CartItem, WishlistItem

from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.wishlist import wishlist_bp
from routes.orders import orders_bp
from routes.outfit import outfit_bp




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connect SQLAlchemy to this Flask application.
    db.init_app(app)

    # Configure user login and session handling.
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Make cart and wishlist counts available to every template.
    @app.context_processor
    def inject_counts():
        if current_user.is_authenticated:
            cart_count = sum(
                item.quantity
                for item in CartItem.query.filter_by(
                    user_id=current_user.id
                ).all()
            )

            wishlist_count = WishlistItem.query.filter_by(
                user_id=current_user.id
            ).count()
        else:
            cart_count = 0
            wishlist_count = 0

        return {
            "cart_count": cart_count,
            "wishlist_count": wishlist_count
        }

    # Register application feature modules.
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(outfit_bp)

    @app.get("/")
    def landing():
        return render_template("landing.html")

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "app": "Eesha's Store"
        }

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                "base.html",
                error_message="The page you requested could not be found."
            ),
            404
        )

    # Create database tables if they do not already exist.
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
