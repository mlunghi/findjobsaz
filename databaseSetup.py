import json
import urllib
import urllib.request
from datetime import date

import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["mainDB"]
feed = db["feed"]
users = db["users"]
