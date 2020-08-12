
import os
import json
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
#client = MongoClient("mongodb+srv://Alnasser0:covid19kfupm@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
db = client['COVID19-KFUPM']
collection = db['COVID19']
#data.reset_index(inplace=True)
#data_dict = data.to_dict("records")
# Read collection
#test = pd.DataFrame(list(collection.find()))
grouped_daily_cities=collection.find_one({"index":"grouped_daily_cities"})
grouped_daily_cities = pd.DataFrame(grouped_daily_cities["data"])
print(grouped_daily_cities.head(5))