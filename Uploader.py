import requests
import os
import shutil
import json
from pymongo import MongoClient
import pandas as pd


url = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
req = requests.get(url)
url_content = req.content
csv_file = open('SA_data.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
data = pd.read_csv("SA_data.csv", sep=None, engine='python') # loading csv file

# Connect to MongoDB
client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")

db = client['COVID19-KFUPM']
collection = db['COVID19']
#data.reset_index(inplace=True)
data_dict = data.to_dict("records")
# Insert collection
collection.delete_one({"index":"SA_data"})
collection.insert_one({"index":"SA_data","data":data_dict})
#collection.insert_many(data_dict)
#insert_many
#insert