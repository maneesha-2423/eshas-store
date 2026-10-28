
from app import app
from models import db, Product, User


# Each product contains:
# name, brand, category, subcategory, price, discount,
# sizes, colour, style_tag and occasion.
SAMPLES = [
    ("Classic Cotton T-Shirt", "Urban Thread", "Men", "Topwear", 799, 20, "S,M,L,XL", "Black", "casual", "everyday"),
    ("Slim Fit Denim Jeans", "Blue Lane", "Men", "Bottomwear", 1499, 15, "28,30,32,34", "Blue", "casual", "everyday"),
    ("Linen Formal Shirt", "North Star", "Men", "Topwear", 1299, 10, "S,M,L,XL", "White", "formal", "work"),
    ("Everyday Polo T-Shirt", "Urban Thread", "Men", "Topwear", 899, 10, "S,M,L,XL", "Navy", "casual", "everyday"),
    ("Chino Trousers", "North Star", "Men", "Bottomwear", 1699, 20, "30,32,34,36", "Beige", "formal", "work"),
    ("Running Sneakers", "Stride", "Men", "Footwear", 2199, 15, "7,8,9,10", "White", "casual", "everyday"),
    ("Printed Kurta", "Aarohi", "Women", "Topwear", 1599, 25, "S,M,L,XL", "Pink", "ethnic", "festive"),
    ("High-Rise Jeans", "Denim Days", "Women", "Bottomwear", 1799, 15, "26,28,30,32", "Blue", "casual", "everyday"),
    ("Floral Summer Dress", "Aarohi", "Women", "Dresses", 1899, 20, "S,M,L,XL", "Yellow", "casual", "brunch"),
    ("Satin Party Top", "Glow Studio", "Women", "Topwear", 1299, 10, "S,M,L,XL", "Black", "party", "party"),
    ("Wide-Leg Trousers", "Glow Studio", "Women", "Bottomwear", 1599, 15, "26,28,30,32", "Black", "party", "party"),
    ("Classic Ballet Flats", "Step Easy", "Women", "Footwear", 999, 10, "5,6,7,8", "Beige", "casual", "everyday"),
    ("Embroidered Anarkali", "Aarohi", "Women", "Dresses", 2999, 20, "S,M,L,XL", "Maroon", "ethnic", "festive"),
    ("Denim Jacket", "Denim Days", "Women", "Topwear", 2199, 10, "S,M,L,XL", "Blue", "casual", "everyday"),
    ("Pleated Midi Skirt", "Glow Studio", "Women", "Bottomwear", 1399, 15, "S,M,L,XL", "Cream", "formal", "work"),
    ("Kids Graphic Tee", "Tiny Trails", "Kids", "Topwear", 499, 10, "2Y,4Y,6Y,8Y", "Yellow", "casual", "everyday"),
    ("Kids Jogger Pants", "Tiny Trails", "Kids", "Bottomwear", 699, 10, "2Y,4Y,6Y,8Y", "Grey", "casual", "everyday"),
    ("Boys Checked Shirt", "Little Legend", "Boys", "Topwear", 799, 10, "4Y,6Y,8Y,10Y", "Blue", "casual", "everyday"),
    ("Boys Cargo Shorts", "Little Legend", "Boys", "Bottomwear", 599, 5, "4Y,6Y,8Y,10Y", "Beige", "casual", "everyday"),
    ("Girls Party Frock", "Petal Pop", "Girls", "Dresses", 1199, 15, "4Y,6Y,8Y,10Y", "Pink", "party", "party"),
    ("Girls Cotton Leggings", "Petal Pop", "Girls", "Bottomwear", 399, 5, "4Y,6Y,8Y,10Y", "Black", "casual", "everyday"),
    ("Kids Hoodie", "Tiny Trails", "Kids", "Topwear", 999, 10, "2Y,4Y,6Y,8Y", "Red", "casual", "winter"),
    ("Gold-Tone Pendant Necklace", "Eesha Jewels", "Jewellery", "Necklaces", 899, 10, "Free Size", "Gold", "ethnic", "festive"),
    ("Pearl Drop Earrings", "Eesha Jewels", "Jewellery", "Earrings", 599, 10, "Free Size", "White", "formal", "party"),
    ("Silver Hoop Earrings", "Moon Metal", "Jewellery", "Earrings", 499, 5, "Free Size", "Silver", "casual", "everyday"),
    ("Layered Gold Necklace", "Eesha Jewels", "Jewellery", "Necklaces", 1299, 15, "Free Size", "Gold", "party", "party"),
    ("Traditional Jhumka Earrings", "Aarohi Jewels", "Jewellery", "Earrings", 799, 10, "Free Size", "Gold", "ethnic", "festive"),
    ("Minimal Silver Bracelet", "Moon Metal", "Jewellery", "Bracelets", 699, 5, "Free Size", "Silver", "formal", "work"),
    ("Beaded Colourful Necklace", "Colour Craft", "Jewellery", "Necklaces", 399, 0, "Free Size", "Multicolour", "casual", "brunch"),
    ("Rose-Gold Stud Earrings", "Eesha Jewels", "Jewellery", "Earrings", 449, 5, "Free Size", "Rose Gold", "formal", "work"),
    ("Men's Leather Belt", "North Star", "Men", "Accessories", 699, 10, "Free Size", "Brown", "formal", "work"),
    ("Men's Casual Hoodie", "Urban Thread", "Men", "Topwear", 1799, 20, "S,M,L,XL", "Grey", "casual", "winter"),
    ("Women's Knit Cardigan", "Glow Studio", "Women", "Topwear", 1699, 10, "S,M,L,XL", "Cream", "casual", "winter"),
    ("Women's Straight Pants", "Glow Studio", "Women", "Bottomwear", 1299, 10, "26,28,30,32", "Black", "formal", "work"),
    ("Kids Canvas Shoes", "Tiny Trails", "Kids", "Footwear", 899, 10, "2,3,4,5", "White", "casual", "everyday"),
    ("Boys Sports Shorts", "Little Legend", "Boys", "Bottomwear", 499, 5, "4Y,6Y,8Y,10Y", "Navy", "casual", "sports"),
    ("Girls Floral Top", "Petal Pop", "Girls", "Topwear", 699, 10, "4Y,6Y,8Y,10Y", "Pink", "casual", "brunch"),
    ("Women's Chiffon Saree", "Aarohi", "Women", "Sarees", 2499, 20, "Free Size", "Maroon", "ethnic", "festive"),
    ("Men's Ethnic Kurta", "North Star", "Men", "Topwear", 1899, 15, "S,M,L,XL", "Cream", "ethnic", "festive"),
    ("Crystal Pendant Set", "Eesha Jewels", "Jewellery", "Necklaces", 1499, 10, "Free Size", "Silver", "party", "party"),
    ("Gold-Plated Bangles", "Aarohi Jewels", "Jewellery", "Bracelets", 999, 10, "2.4,2.6,2.8", "Gold", "ethnic", "festive"),
    ("Girls Denim Jacket", "Petal Pop", "Girls", "Topwear", 1099, 10, "4Y,6Y,8Y,10Y", "Blue", "casual", "everyday"),
    ("Men's Running Shoes", "Stride", "Men", "Footwear", 2499, 15, "7,8,9,10", "Black", "casual", "sports"),
    ("Women's Block Heels", "Step Easy", "Women", "Footwear", 1799, 10, "5,6,7,8", "Beige", "party", "party"),
    ("Kids Printed Night Suit", "Tiny Trails", "Kids", "Nightwear", 799, 10, "2Y,4Y,6Y,8Y", "Blue", "casual", "sleep"),
    ("Boys Festive Kurta", "Little Legend", "Boys", "Topwear", 999, 10, "4Y,6Y,8Y,10Y", "White", "ethnic", "festive"),
    ("Women's Classic Handbag", "Glow Studio", "Women", "Accessories", 1999, 10, "Free Size", "Black", "formal", "work"),
    ("Oxidised Silver Choker", "Moon Metal", "Jewellery", "Necklaces", 1099, 15, "Free Size", "Silver", "ethnic", "festive"),
    ("Colour Pop Studs", "Colour Craft", "Jewellery", "Earrings", 299, 0, "Free Size", "Multicolour", "casual", "everyday"),
    ("Men's Cotton Shorts", "Urban Thread", "Men", "Bottomwear", 799, 10, "30,32,34,36", "Olive", "casual", "summer"),
]


def seed_products():
    # Avoid inserting duplicate products every time the seed script runs.
    if Product.query.count() > 0:
        print(f"Products already exist ({Product.query.count()}); skipping product seed.")
        return

    for index, row in enumerate(SAMPLES):
        (
            name, brand, category, subcategory, price, discount,
            sizes, colour, style, occasion
        ) = row

        product = Product(
            name=name,
            brand=brand,
            category=category,
            subcategory=subcategory,
            price=price,
            discount=discount,
            sizes=sizes,
            colour=colour,
            style_tag=style,
            occasion=occasion,
            image=f"https://picsum.photos/seed/eesha{index + 1}/700/850",
            rating=round(3.6 + (index % 14) * 0.1, 1),
            stock=8 + index % 20,
            popularity=100 - index,
            description=(
                f"{name} by {brand}. A thoughtfully selected piece "
                "for your wardrobe. Check the size and care details "
                "before ordering."
            )
        )
        db.session.add(product)

    print(f"Added {len(SAMPLES)} sample products.")


def seed_admin():
    admin_email = "admin@eeshasstore.local"

    if User.query.filter_by(email=admin_email).first():
        print("Demo admin already exists.")
        return

    admin = User(
        name="Store Admin",
        email=admin_email,
        is_admin=True
    )
    admin.set_password("Admin@12345")
    db.session.add(admin)

    print("Created demo admin: admin@eeshasstore.local")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        try:
            seed_products()
            seed_admin()
            db.session.commit()
            print("Database seeding completed successfully.")
        except Exception:
            db.session.rollback()
            raise
