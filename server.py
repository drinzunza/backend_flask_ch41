from flask import Flask, request, abort
from config import me
from mock_data import catalog, coupon_codes
import json


app = Flask(__name__)

@app.get("/")
def index():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is another page"


#############################################
#############   API    ######################
#############################################

@app.get("/api/version")
def version():
    v = {
        "version": "1.0.0",
        "name": "Genesis"
    }
    return json.dumps(v)



@app.get("/api/about")
def about():
    return json.dumps(me)


@app.get('/api/catalog')
def get_catalog():
    return json.dumps(catalog)



@app.post('/api/catalog')
def save_product():
    product = request.get_json()

    product["_id"] = len(catalog)
    catalog.append(product)

    return json.dumps(product)


@app.get("/api/report/total")
def report_total():
    
    total = 0
    for prod in catalog:
        # total = total + prod["price"]
        total += prod["price"]

    result = {
        "report": "total",
        "value": total
    }
    return json.dumps(result)



# get all products for a given category
@app.get("/api/products/<cat>")
def get_by_category(cat):
    results = []
    for prod in catalog:
        if prod["category"] == cat:
            results.append(prod)

    return json.dumps(results)




# get search  <term>
@app.get("/api/products/search/<term>")
def product_search(term):
    results = []
    for prod in catalog:
        if term.lower() in prod['title'].lower():
            results.append(prod)

    return json.dumps(results)



# create an endpoint to get all the products with a price
# lower or equal than a given number
@app.get("/api/products/lower/<price>")
def products_lower(price):
    results = []
    real_price = float(price)
    
    for prod in catalog:
        if prod['price'] <= real_price:
            results.append(prod)

    return json.dumps(results)






#############################################
#############   COUPONS   ###################
#############################################

@app.get("/api/coupons")
def get_coupons():
    return json.dumps(coupon_codes)


@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    coupon["_id"] = len(coupon_codes)

    coupon_codes.append(coupon)
    return json.dumps(coupon)



# get  /api/coupons/<code>
# search for the coupon with the code
# and return the obj/dict if exist
@app.get("/api/coupons/<code>")
def search_coupon(code):
    for coupon in coupon_codes:
        if coupon["code"].lower() == code.lower():
            return json.dumps(coupon)
        
    return abort(404, "Invalid Coupon Code")


# app.run(debug=True)