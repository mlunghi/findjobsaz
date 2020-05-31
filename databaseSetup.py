import json
import urllib
import urllib.request
from datetime import date

import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["mainDB"]

users = db["users"]
users.drop()
to_load = {
    "email": "hello",
    "brown_id": "hzaki",
}
print(to_load)
users.insert_one(to_load)
print("hello")
