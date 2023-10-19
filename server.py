from flask import Flask
from config import me
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

app.run(debug=True)