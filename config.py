
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Keep secret values in environment variables for better security.
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-secret-before-deployment"
    )

    # SQLite database is stored inside the project folder.
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "eeshas_store.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie security settings.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
