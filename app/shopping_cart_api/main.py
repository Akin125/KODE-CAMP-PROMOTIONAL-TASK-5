from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from cart import add_to_cart, checkout_cart
import json

app = FastAPI()

PRODUCTS_FILE = "product.json"

class Product(BaseModel):
    id: int
    name: str
    price: float

@app.get("/products/")
def list_products():
    try:
        with open(PRODUCTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cart/add")
def add_product_to_cart(product_id: int = Query(...), qty: int = Query(...)):
    return add_to_cart(product_id, qty)

@app.get("/cart/checkout")
def checkout():
    return checkout_cart()