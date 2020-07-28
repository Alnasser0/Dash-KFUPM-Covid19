import requests
import os
import shutil

url = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
req = requests.get(url)
url_content = req.content
csv_file = open('SA_data.csv', 'wb')
csv_file.write(url_content)
csv_file.close()