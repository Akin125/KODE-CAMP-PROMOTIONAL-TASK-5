"""
Shopping Cart API

A FastAPI application for managing a simple e-commerce shopping cart system.
Provides endpoints for managing products and cart operations with JSON storage.

Features:
    - Product management (add, list products)
    - Cart operations (add items, view cart, checkout)
    - Persistent storage using JSON files
    - Basic error handling
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from cart import add_to_cart, load_cart, load_products, checkout_cart, clear_cart

app = FastAPI(
    title="Shopping Cart API",
    description="Simple e-commerce shopping cart management system",
    version="1.0.0"
)

class Product(BaseModel):
    """
    Represents a product in the inventory.

    Attributes:
        id (int): Unique product identifier
        name (str): Product name
        price (float): Product price
        description (str): Product description
    """
    id: int
    name: str
    price: float
    description: str

class CartItem(BaseModel):
    """
    Represents an item in the shopping cart.

    Attributes:
        product_id (int): ID of the product to add
        quantity (int): Quantity to add to cart
    """
    product_id: int
    quantity: int

@app.post("/products/")
def add_product(product: Product):
    """
    Add a new product to the inventory.

    Args:
        product (Product): The product to add

    Returns:
        dict: Success message and product details

    Raises:
        HTTPException: If there's an error adding the product
    """
    try:
        products = load_products()
        if any(p['id'] == product.id for p in products):
            raise HTTPException(status_code=400, detail="Product ID already exists")

        products.append(product.dict())
        with open('product.json', 'w') as f:
            json.dump(products, f, indent=4)

        return {"message": "Product added successfully", "product": product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/")
def list_products():
    """
    List all products in the inventory.

    Returns:
        list: List of all products

    Raises:
        HTTPException: If there's an error retrieving products
    """
    try:
        return load_products()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cart/add")
def add_item_to_cart(item: CartItem):
    """
    Add an item to the shopping cart.

    Args:
        item (CartItem): The item to add to cart

    Returns:
        dict: Success message

    Raises:
        HTTPException: If there's an error adding the item
    """
    try:
        result = add_to_cart(item.product_id, item.quantity)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cart/")
def view_cart():
    """
    View the current contents of the shopping cart.

    Returns:
        list: Current cart contents

    Raises:
        HTTPException: If there's an error retrieving the cart
    """
    try:
        return load_cart()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cart/checkout")
def process_checkout():
    """
    Process checkout for the current cart.

    Returns:
        dict: Checkout summary including total price and items

    Raises:
        HTTPException: If there's an error during checkout
    """
    try:
        result = checkout_cart()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cart/clear")
def clear_shopping_cart():
    """
    Remove all items from the shopping cart.

    Returns:
        dict: Success message

    Raises:
        HTTPException: If there's an error clearing the cart
    """
    try:
        return clear_cart()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
