
# Eesha's Store — Fashion & Jewellery E-commerce

## Project Description

Eesha's Store is a full-stack e-commerce web application
for fashion clothing, accessories and jewellery.

It is built using Python Flask, SQLite, SQLAlchemy,
HTML, CSS, JavaScript and Jinja2 templates.

The project is designed as a portfolio project for
learning full-stack development and demonstrating
practical software engineering skills.

## Features

- Responsive landing page and product catalogue.
- User registration, login and logout.
- Secure password hashing.
- Men, Women, Boys, Girls, Kids and Jewellery categories.
- Product search and category filtering.
- Price, size, brand and rating filters.
- Product sorting by price, newest and popularity.
- Product details and size selection.
- Shopping cart and wishlist.
- Checkout with Cash on Delivery.
- Order confirmation and order history.
- Outfit Match using colour, style and occasion.
- Admin product management.
- SQLite database and sample product data.

## Technology Stack

Frontend:
- HTML5
- CSS3
- JavaScript
- Bootstrap-compatible responsive design principles
- Jinja2 templates

Backend:
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

Database:
- SQLite

Development tools:
- Visual Studio Code
- Git and GitHub

## Project Structure

shopping_app/
    app.py
    config.py
    models.py
    seed.py
    requirements.txt
    README.md
    routes/
        __init__.py
        auth.py
        products.py
        cart.py
        wishlist.py
        orders.py
        outfit.py
    templates/
        base.html
        landing.html
        home.html
        category.html
        product.html
        cart.html
        wishlist.html
        checkout.html
        orders.html
        login.html
        register.html
        outfit.html
    static/
        css/
            style.css
        js/
            main.js
        images/

## Installation and Setup

### Step 1: Install Python

Install Python 3.10 or a compatible newer version.
During installation, enable the option to add Python to PATH.

### Step 2: Open the project

Open the shopping_app folder in Visual Studio Code.

### Step 3: Create a virtual environment

Windows PowerShell:

    py -m venv .venv

### Step 4: Activate the environment

    .\.venv\Scripts\Activate.ps1

If PowerShell blocks activation:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\.venv\Scripts\Activate.ps1

### Step 5: Install dependencies

    python -m pip install --upgrade pip
    pip install -r requirements.txt

### Step 6: Create sample data

    python seed.py

This creates the database tables, adds sample products
and creates the local demo admin account.

### Step 7: Start the application

    python app.py

### Step 8: Open the website

    http://127.0.0.1:5000

## Demo Admin Account

Email: admin@eeshasstore.local
Password: Admin@12345

Admin page:
http://127.0.0.1:5000/admin/products

Change the demo password and secret key before deployment.

## Database

The application uses SQLite.

Database filename:
eeshas_store.db

The database tables are created automatically when
the Flask application starts.

## Outfit Match

The Outfit Match feature evaluates the selected topwear,
bottomwear and jewellery using a rule-based scoring system.

It considers:
- Colour compatibility.
- Style compatibility.
- Occasion compatibility.

The application produces a score, a verdict and
suggestions for alternative products.

## Five Resume Bullet Points

1. Developed a responsive full-stack fashion and jewellery
   e-commerce application using Python Flask and SQLite.

2. Implemented user authentication, password hashing
   and session management using Flask-Login.

3. Built product discovery features including keyword
   search, sorting and combined catalogue filters.

4. Implemented cart, wishlist, checkout, Cash on Delivery
   and order history workflows.

5. Designed an explainable outfit recommendation feature
   using colour, style and occasion compatibility rules.

## Future Improvements

- Add automated unit and integration tests.
- Add CSRF protection and stronger security controls.
- Implement product editing and stock management.
- Add pagination and improved search.
- Add a production-ready payment gateway if required.
- Deploy using a production WSGI server.
- Replace placeholder images with locally stored images.

## Important Note

This is a learning and portfolio application.
Do not use the development secret key or demo admin
credentials in a public production deployment.
