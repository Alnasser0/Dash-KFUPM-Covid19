from app import app

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

client = MongoClient(
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@covid19-kfupm.8orak.azure.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"
)
db = client[DB_NAME]
regions_collection = db['regions']
cities_collection = db['cities']


@app.route('/')
@app.route('/index')
def index():
    return dumps(regions_collection.find())
