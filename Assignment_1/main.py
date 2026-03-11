from fastapi import FastAPI, Query
app = FastAPI()

products = [
    {"id": 1, "name": "wireless mouse", "price": 25.99, "category": "electronics", "in_stock": True},
    {"id": 2, "name": "Bluetooth headphones", "price": 59.99, "category": "electronics", "in_stock": True},
    {"id": 3, "name": "coffee mug", "price": 9.99, "category": "kitchen", "in_stock": False},
    {"id": 4, "name": "notebook", "price": 2.99, "category": "stationery", "in_stock": True},
    {"id": 5, "name": "pen set", "price": 5.49, "category": "stationery", "in_stock": False},
    {"id": 6, "name": "desk lamp", "price": 19.99, "category": "electronics", "in_stock": True},
    {"id": 7, "name": "water bottle", "price": 14.99, "category": "kitchen", "in_stock": True},
]

@app.get('/')
def home():
    return {"message": "Welcome to our E-Commerce app"}   

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationery'),
    max_price: int = Query(None, description='Maximum price'),
    in_stock: bool = Query(None, description='True = in stock only')
):
    result = products
    # Start with all products
    if category:
        result = [p for p in result if p['category'] == category]
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return {'filtered_products': result, 'count': len(result)}

@app.get('/products/category/{category_name}')
def get_products_by_category(category_name: str):
    result = [p for p in products if p['category'] == category_name]
    return {'products': result, 'count': len(result)}

@app.get('/products/instock')
def get_in_stock_products():
    result = [p for p in products if p['in_stock']]
    return {'products': result, 'count': len(result)}

@app.get('/products/summary')
def get_products_summary():
    total_products = len(products)
    store_name = "My E-Commerce Store"
    in_stock_products = len([p for p in products if p['in_stock']])
    out_of_stock_products = total_products - in_stock_products
    categories = set(p['category'] for p in products)
    return {
        'total_products': total_products,
        'store_name': store_name,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'categories': list(categories)
    }


@app.get("/products/search/{keyword}")
def search_products(keyword: str): 
    results = [ p for p in products if keyword.lower() in p["name"].lower() ] 
    if not results: 
        return {"message": "No products matched your search"} 
    return {"keyword": keyword, "results": results, "total_matches": len(results)}

@app.get('/products/deals')
def get_deals(): 
    cheapest = min(products, key=lambda p: p["price"]) 
    expensive = max(products, key=lambda p: p["price"]) 
    return { "best_deal": cheapest, "premium_pick": expensive, }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}

