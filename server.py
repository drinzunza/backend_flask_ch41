from flask import Flask, request, abort
from config import me, db
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

def fix_id(record):
    record["_id"] = str(record["_id"])
    return record

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
    cursor = db.products.find({})
    results = []

    for product in cursor:
        fix_id(product)
        results.append(product)

    return json.dumps(results)


@app.post('/api/catalog')
def save_product():
    product = request.get_json()

    # save product to db
    db.products.insert_one(product)

    return json.dumps(fix_id(product))


@app.get("/api/report/total")
def report_total():
    cursor = db.products.find({})
    total = 0
    for prod in cursor:
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
    cursor = db.products.find({ "category": cat })
    results = []
    for prod in cursor:        
        fix_id(prod)
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
    cursor = db.products.find({ 'price': {'$lte': real_price }})
    
    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)



# get price greater or equal
@app.get("/api/products/greater/<price>")
def products_greater(price):
    results = []
    real_price = float(price)
    cursor = db.products.find({'price': {'$gte': real_price}})

    for prod in cursor:
        fix_id(prod)
        results.append(prod)

    return json.dumps(results)


#############################################
#############   COUPONS   ###################
#############################################

@app.get("/api/coupons")
def get_coupons():
    cursor = db.coupons.find({})
    results = []
    for coupon in cursor:
        fix_id(coupon)
        results.append(coupon)

    return json.dumps(results)


@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()
    db.coupons.insert_one(coupon)
    fix_id(coupon)

    return json.dumps(coupon)



# get  /api/coupons/<code>
# search for the coupon with the code
# and return the obj/dict if exist
@app.get("/api/coupons/<code>")
def search_coupon(code):
    coupon = db.coupons.find_one({"code": {'$regex': f"^{code}$", '$options': "i"}})
    if not coupon:  
        return abort(404, "Invalid Coupon Code")
    
    fix_id(coupon)
    return json.dumps(coupon)


# app.run(debug=True)