from fastapi import FastAPI, HTTPException
from models.product import Product
import sqlite3
app = FastAPI()

def mappingProduct(products: list):
    result = []
    for product in products:
        result.append(Product(product[0], product[1], product[2]))
    return result

@app.get("/products")
async def get_products():
    products = []
    with sqlite3.connect("eshop.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, price FROM products")
        products = cursor.fetchall()
    return mappingProduct(products)

@app.get("/products")
async def get_min_max_products(priceMin: int, priceMax: int):
    with sqlite3.connect("eshop.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, price FROM products WHERE price BETWEEN ? AND ?", (priceMin, priceMax))
        products = cursor.fetchall()
    return mappingProduct(products)

@app.post("/products")
def create_product(product: dict):
    with sqlite3.connect("eshop.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO products(title, price) VALUES(?,?)", (product["title"], product["price"]))
        connection.commit()
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: dict):
    with sqlite3.connect("eshop.db") as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE products SET title = ?, price = ? WHERE id = ?", (product["title"],product["price"],product_id))
        connection.commit()
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with sqlite3.connect("eshop.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        connection.commit()
        products = cursor.fetchall()
    return mappingProduct(products)


