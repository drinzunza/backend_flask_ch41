import pymongo
import certifi

me = {
    "first_name": "Sergio",
    "last_name": "Inzunza",
    "email": "sinzunza@sdgku.edu",
    "github": "https://github.com/drinzunza"
}


con_str = "mongodb+srv://fsdi:Test1234@cluster0.wodxmeh.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("organika")