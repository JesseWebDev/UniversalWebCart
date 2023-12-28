from flask import Flask, render_template, request, session, redirect, url_for
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for sessions



# Function to fetch product details from a URL
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

# Function to load user-specific products from a JSON file based on user session
def load_user_products():
    if 'user_products' in session:
        return session['user_products']
    else:
        return []

# Function to save user-specific products to the session
def save_user_products(user_products):
    session['user_products'] = user_products



# Define the function to handle adding a product
@app.route('/add_product', methods=['POST'])
def handle_add_product():
    if request.method == 'POST':
        url = request.form['url']
        price = request.form['price']

        if not price:
            price = 'Price Not Found'  # Set a default value when the price field is empty
        else:
            price = f'${price}'  # Prepend the dollar sign to the price value

        product_details = get_product_details(url)

        if product_details:
            product_name, product_price, product_image = product_details

            user_products = load_user_products()

            existing_urls = [product['url'] for product in user_products]

            if url not in existing_urls:
                new_id = len(user_products) + 1
                new_product = {'id': new_id, 'name': product_name, 'price': price, 'url': url, 'image': product_image}
                user_products.append(new_product)

                # Save updated user-specific products to the session
                save_user_products(user_products)
                print("Product added successfully!")

    return redirect(url_for('index'))

# Define other routes...

@app.route('/')
def index():
    user_products = load_user_products()
    return render_template('index.html', products=user_products)

# Other routes and functions...

if __name__ == '__main__':
    app.run(debug=True)
