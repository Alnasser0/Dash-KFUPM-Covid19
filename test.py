
import os
import json
from pymongo import MongoClient
import pandas as pd


data = pd.read_csv("SA_data.csv", sep=None, engine='python') # loading csv file
#data.to_json('yourjson.json')                               # saving to json file
#jdf = open('yourjson.json').read()                          # loading the json file 
#data = json.loads(jdf)                                      # reading json file 


# Connect to MongoDB
#client = MongoClient("mongodb+srv://Alnasser0:covid19kfupm@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
db = client['COVID19-KFUPM']
collection = db['COVID19']
#data.reset_index(inplace=True)
data_dict = data.to_dict("records")
# Insert collection
#collection.delete_many({})
collection.insert_one({"index":"SA_data","data":data_dict})
#collection.insert_many(data_dict)