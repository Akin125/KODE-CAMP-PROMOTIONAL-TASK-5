import json
import os

CART_FILE = "cart_data.json"
PRODUCTS_FILE = "product.json"  # Fixed filename

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r') as f:
        return json.load(f)

def load_cart():
    if not os.path.exists(CART_FILE):
        return []
    with open(CART_FILE, 'r') as f:
        return json.load(f)

def save_cart(cart):
    with open(CART_FILE, 'w') as f:
        json.dump(cart, f, indent=4)

def add_to_cart(product_id, qty):
    try:
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")

        products = load_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            raise ValueError("Product not found")

        cart = load_cart()
        # Check if product already exists in cart
        existing_item = next((item for item in cart if item['id'] == product_id), None)

        if existing_item:
            existing_item['qty'] += qty
        else:
            cart.append({
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "qty": qty
            })

        save_cart(cart)
        return {"message": "Product added to cart successfully"}
    except Exception as e:
        raise ValueError(str(e))

def checkout_cart():
    try:
        cart = load_cart()
        if not cart:
            return {"message": "Cart is empty"}

        total = sum(item['price'] * item['qty'] for item in cart)

        # Clear the cart after checkout
        save_cart([])

        return {
            "message": "Checkout successful",
            "total_price": round(total, 2),
            "items": cart
        }
    except Exception as e:
        raise ValueError(str(e))
