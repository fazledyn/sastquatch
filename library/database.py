from pymongo import MongoClient
import os


db = None
mongo = None
user_collection = None
package_collection = None
problem_collection = None


def load_database():
    global db
    global mongo
    global user_collection 
    global package_collection 
    global problem_collection

    mongo = MongoClient(os.getenv("MONGO_URI"))
    db = mongo.get_database(os.getenv("MONGO_DATABASE"))
    user_collection = db.get_collection(os.getenv("USER_COLLECTION"))
    package_collection = db.get_collection(os.getenv("PACKAGE_COLLECTION"))
    problem_collection = db.get_collection(os.getenv("PROBLEM_COLLECTION"))
