import os
import time
import json
import requests

import numpy as np
import pandas as pd

from models.city import City
from models.region import Region
from models.total import Total

from dotenv import load_dotenv
from pymongo import MongoClient

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

start = time.time()
URL = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
response = requests.get(URL)
content = response.content

print(f"Time taken (s) to download the file: {time.time() - start}")
file_name = 'SA_data.csv'

start = time.time()
with open(file_name, 'wb') as csv_file:
    csv_file.write(content)

# loading csv file
all_data = pd.read_csv(file_name, sep=';',
                       engine='c', encoding='utf-8',
                       dtype={'Daily / Cumulative': object, 'Indicator': object, 'Event': object, 'City': object, 'Region': object})

# TODO: Check if required columns exists before parsing

# General clean
all_data = all_data.rename(
    columns={'Cases (person)': 'Cases', 'Daily / Cumulative': 'D/C'}
)
# For daily, replace 'Cases' with 'New Cases'
all_data.loc[(all_data['D/C'] == 'Daily') & (all_data['Indicator'] == 'Cases'), 'Indicator'] = 'New Cases'
# For cumulative, replace 'Cases' with 'Confirmed'
all_data.loc[(all_data['D/C'] == 'Cumulative') & (all_data['Indicator'] == 'Cases'), 'Indicator'] = 'Confirmed'
all_data = all_data.sort_values(by='Date')

# Extract total data (all regions)
df_total = all_data[all_data['Region'] == 'Total']
df_total = df_total.drop(columns=['Region', 'City'])

# Total daily
df_total_daily = df_total[df_total['D/C'] == 'Daily'].pivot(
    index='Date', columns='Indicator', values=['Cases']
).fillna(0).astype('int64')
df_total_daily.columns = df_total_daily.columns.droplevel(0)
df_total_daily = df_total_daily.reset_index().rename_axis(None, axis=1)

# Total cumulative
df_total_cumulative = df_total[df_total['D/C'] == 'Cumulative'].pivot(
    index='Date', columns='Indicator', values=['Cases']
).fillna(0).astype('int64')
df_total_cumulative.columns = df_total_cumulative.columns.droplevel(0)
df_total_cumulative = df_total_cumulative.reset_index().rename_axis(None, axis=1)

total = Total(id='All Regions')
total.daily = df_total_daily.to_dict('records')
total_cumulative_list = df_total_cumulative.to_dict('records')
total.cumulative = total_cumulative_list
total.confirmed = total_cumulative_list[-1]['Confirmed']
total.active = total_cumulative_list[-1]['Active']
total.tested = total_cumulative_list[-1]['Tested']
total.critical = total_cumulative_list[-1]['Critical']
total.recoveries = total_cumulative_list[-1]['Recoveries']
total.mortalities = total_cumulative_list[-1]['Mortalities']

# Extract daily data
df_daily = all_data[(all_data['D/C'] == 'Daily') & (all_data['Region'] != 'Total')]

# Extract cumulative data
df_cumulative = all_data[(all_data['D/C'] == 'Cumulative') & (all_data['Region'] != 'Total')]

# Pivot region data
df_regions_daily_pivoted = df_daily.pivot_table(
    index=['Region', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=True, aggfunc=np.sum
)

df_regions_daily_pivoted = df_regions_daily_pivoted.reset_index(level='Date')

df_regions_cumulative_pivoted = df_cumulative.pivot_table(
    index=['Region', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=True, aggfunc=np.sum
)
df_regions_cumulative_pivoted = df_regions_cumulative_pivoted.reset_index(level='Date')

# Region - Cities
df_regions_cities = df_cumulative.pivot_table(index=['Region', 'City']).reset_index(level='City')

region_names = list(df_regions_daily_pivoted.index.unique(level=0))

all_regions = []
for region in region_names:
    r = Region(name=region)
    r.daily = df_regions_daily_pivoted.loc[region].to_dict('records')
    region_cumulative = df_regions_cumulative_pivoted.loc[region].to_dict('records')
    r.cumulative = region_cumulative
    r.active = region_cumulative[-1]['Active']
    r.confirmed = region_cumulative[-1]['Confirmed']
    r.mortalities = region_cumulative[-1]['Mortalities']
    r.recoveries = region_cumulative[-1]['Recoveries']
    r.cities = df_regions_cities.loc[region]['City'].tolist()

    all_regions.append(r.__dict__)

# Pivot city data
df_cities_daily_pivoted = df_daily.pivot_table(
    index=['City', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=True, aggfunc=np.sum
)
df_cities_daily_pivoted = df_cities_daily_pivoted.reset_index(level='Date')

df_cities_cumulative_pivoted = df_cumulative.pivot_table(
    index=['City', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=True, aggfunc=np.sum
)
df_cities_cumulative_pivoted = df_cities_cumulative_pivoted.reset_index(level='Date')

city_names = list(df_cities_daily_pivoted.index.unique(level=0))

all_cities = []
for city in city_names:
    c = City(name=city)
    c.daily = df_cities_daily_pivoted.loc[city].to_dict('records')
    city_cumulative = df_cities_cumulative_pivoted.loc[city].to_dict('records')
    c.cumulative = city_cumulative
    c.active = city_cumulative[-1]['Active']
    c.confirmed = city_cumulative[-1]['Confirmed']
    c.mortalities = city_cumulative[-1]['Mortalities']
    c.recoveries = city_cumulative[-1]['Recoveries']

    all_cities.append(c.__dict__)


# Insert Data
regions_collection.delete_many({})
cities_collection.delete_many({})

regions_collection.insert_one(total.__dict__)
regions_collection.insert_many(all_regions)
cities_collection.insert_many(all_cities)

print(f"Time taken (s) to insert all documents: {time.time()-start}")
