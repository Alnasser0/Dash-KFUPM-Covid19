import time
import json
import requests

import numpy as np
import pandas as pd

from models.city import City
from models.region import Region
from models.total import Total

from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://ajmal-ali:JTLrQEUoEn7VcSj3@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority"
)
db = client['COVID19-KFUPM']
regions_collection = db['regions']
cities_collection = db['cities']

regions_collection.delete_many({})
cities_collection.delete_many({})

URL = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
response = requests.get(URL)
content = response.content

file_name = 'SA_data.csv'

with open(file_name, 'wb') as csv_file:
    csv_file.write(content)

# loading csv file
all_data = pd.read_csv(file_name, sep=';',
                       engine='c', encoding='utf-8')

# TODO: Check if required columns exists before parsing

# General clean
all_data = all_data.rename(
    columns={'Cases (person)': 'Cases', 'Daily / Cumulative': 'D/C'}
)
# For daily, replace 'Cases' with 'New Cases'
all_data.loc[(all_data['D/C'] == 'Daily') &
             (all_data['Indicator'] == 'Cases'), 'Indicator'] = 'New Cases'
# For cumulative, replace 'Cases' with 'Confirmed'
all_data.loc[(all_data['D/C'] == 'Cumulative') &
             (all_data['Indicator'] == 'Cases'), 'Indicator'] = 'Confirmed'
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
total.cumualtive = total_cumulative_list
total.confirmed = total_cumulative_list[-1]['Confirmed']
total.active = total_cumulative_list[-1]['Active']
total.tested = total_cumulative_list[-1]['Tested']
total.critical = total_cumulative_list[-1]['Critical']
total.recoveries = total_cumulative_list[-1]['Recoveries']
total.mortalities = total_cumulative_list[-1]['Mortalities']

regions_collection.insert_one(total.__dict__)

# Extract daily data
df_daily = all_data[(all_data['D/C'] == 'Daily') &
                    (all_data['Region'] != 'Total')]

# Extract cumulative data
df_cumulative = all_data[(all_data['D/C'] == 'Cumulative')
                         & (all_data['Region'] != 'Total')]

# Pivot region data
df_regions_daily_pivoted = df_daily.pivot_table(
    index=['Region', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=False, aggfunc=np.sum
)
df_regions_daily_pivoted = df_regions_daily_pivoted.reset_index(level='Date')

df_regions_cumulative_pivoted = df_cumulative.pivot_table(
    index=['Region', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=False, aggfunc=np.sum
)
df_regions_cumulative_pivoted = df_regions_cumulative_pivoted.reset_index(
    level='Date')

region_names = list(df_regions_daily_pivoted.index.unique(level=0))

all_regions = []
for region in region_names:
    r = Region(name=region)
    r.daily = df_regions_daily_pivoted.loc[region].to_dict('records')
    region_cumulative = df_regions_cumulative_pivoted.loc[region].to_dict(
        'records'
    )
    r.cumualtive = region_cumulative
    r.active = region_cumulative[-1]['Active']
    r.confirmed = region_cumulative[-1]['Confirmed']
    r.mortalities = region_cumulative[-1]['Mortalities']
    r.recoveries = region_cumulative[-1]['Recoveries']

    all_regions.append(r.__dict__)

regions_collection.insert_many(all_regions)

# Pivot city data
df_cities_daily_pivoted = df_daily.pivot_table(
    index=['City', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=False, aggfunc=np.sum
)

df_cities_cumulative_pivoted = df_cumulative.pivot_table(
    index=['City', 'Date'], columns='Indicator', values='Cases', fill_value=0, dropna=False, aggfunc=np.sum
)

city_names = list(df_cities_daily_pivoted.index.unique(level=0))

all_cities = []
for city in city_names:
    c = City(name=city)
    c.daily = df_cities_daily_pivoted.loc[city].to_dict('records')
    city_cumulative = df_cities_cumulative_pivoted.loc[city].to_dict(
        'records'
    )
    c.cumualtive = city_cumulative
    c.active = city_cumulative[-1]['Active']
    c.confirmed = city_cumulative[-1]['Confirmed']
    c.mortalities = city_cumulative[-1]['Mortalities']
    c.recoveries = city_cumulative[-1]['Recoveries']

    all_cities.append(c.__dict__)

cities_collection.insert_many(all_cities)
