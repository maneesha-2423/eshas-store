
# Eesha's Store — Images

Store your own product images and branding assets in this directory.

Suggested structure:

images/
├── logo.png
├── hero-fashion.jpg
├── categories/
│   ├── women.jpg
│   ├── men.jpg
│   ├── kids.jpg
│   └── jewellery.jpg
└── products/
    ├── product-001.jpg
    ├── product-002.jpg
    └── product-003.jpg

## Referencing images in Flask templates

Logo:
{{ url_for('static', filename='images/logo.png') }}

Hero banner:
{{ url_for('static', filename='images/hero-fashion.jpg') }}

Product image paths should be saved in the database as relative paths such as:
images/products/product-001.jpg

Only use images you own or have permission to use.
