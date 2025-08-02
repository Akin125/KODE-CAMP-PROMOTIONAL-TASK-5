"""
Shopping Cart Module

This module handles the core shopping cart functionality including:
- Loading and saving cart data
- Managing product inventory
- Adding items to cart
- Calculating totals

The module uses JSON files for persistent storage of both products and cart data.
"""

import json
import os

CART_FILE = "cart_data.json"
PRODUCTS_FILE = "product.json"

def load_products() -> list:
    """
    Load product inventory from JSON file.

    Returns:
        list: List of product dictionaries, empty list if file doesn't exist
    """
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r') as f:
        return json.load(f)

def load_cart() -> list:
    """
    Load current cart contents from JSON file.

    Returns:
        list: List of cart items, empty list if file doesn't exist
    """
    if not os.path.exists(CART_FILE):
        return []
    with open(CART_FILE, 'r') as f:
        return json.load(f)

def save_cart(cart: list) -> None:
    """
    Save cart contents to JSON file.

    Args:
        cart (list): List of cart items to save
    """
    with open(CART_FILE, 'w') as f:
        json.dump(cart, f, indent=4)

def add_to_cart(product_id: int, qty: int) -> dict:
    """
    Add a product to the shopping cart.

    Args:
        product_id (int): ID of the product to add
        qty (int): Quantity to add

    Returns:
        dict: Success message

    Raises:
        ValueError: If quantity is invalid or product not found
    """
    try:
        # Validate quantity
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")

        # Find product in inventory
        products = load_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            raise ValueError("Product not found")

        # Load current cart and check for existing item
        cart = load_cart()
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
    """
    Checkout the current cart, calculating total price and clearing the cart.

    Returns:
        dict: Checkout summary including total price and cart items

    Raises:
        ValueError: If there is an error during checkout process
    """
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

def get_cart_total() -> float:
    """
    Calculate the total value of items in the cart.

    Returns:
        float: Total cart value
    """
    cart = load_cart()
    return sum(item['price'] * item['qty'] for item in cart)

def clear_cart() -> dict:
    """
    Remove all items from the cart.

    Returns:
        dict: Success message
    """
    save_cart([])
    return {"message": "Cart cleared successfully"}
