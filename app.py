from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Initial list of predefined products
products = [

    # Add more products here
]

def get_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product name from the webpage title
    product_name = soup.title.string if soup.title else 'Product Name Not Found'

    # Extract product price
    price_element = soup.find('span', class_='product-price')  # Replace with the actual price element
    product_price = price_element.text.strip() if price_element else None

    # Extract product image URL
    image_element = soup.find('img', class_='product-image')  # Replace with the actual image element
    product_image = image_element['src'] if image_element and 'src' in image_element.attrs else None

    return product_name, product_price, product_image

# Define the function to handle adding a product
def handle_add_product():
    if request.method == 'POST':
        url = request.form['url']
        price = request.form['price']

        if not price:
            price = 'Price Not Found'  # Set a default value when the price field is empty
        else:
            price = f'${price}'  # Prepend the dollar sign to the price value

        product_name, product_price, product_image = get_product_details(url)

        existing_urls = [product['url'] for product in products]

        if url not in existing_urls:
            new_id = len(products) + 1
            new_product = {'id': new_id, 'name': product_name, 'price': price, 'url': url, 'image': product_image}
            products.append(new_product)

        return render_template('index.html', products=products)

# Map the function to the desired route
app.add_url_rule('/add_product', 'add_product', handle_add_product, methods=['POST'])

# Index route
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Delete product route
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    global products
    products = [product for product in products if product['id'] != product_id]
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
