
import wget
import os
import shutil

url = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
wget.download(url, "SA_data.csv")
if os.path.exists("SA_data.csv"):
    shutil.move("SA_data (1).csv","SA_data.csv")