
from pymongo import MongoClient
from pathlib import Path
import csv
from bson import Int64, Decimal128
from datetime import datetime
import pandas as pd
from pandas import Series
import numpy as np
import os
import math


MONGODB_URI = "mongodb://192.168.0.204:27017/"

client = MongoClient(MONGODB_URI)
db = client["marketdata"]
market_data_collections = list()


def get_one(col_name: str):
    col = db[col_name]
    res = col.find_one({})
    return res

def get_all(col_name: str):
    col = db[col_name]
    res = col.find()
    return res


def load_market_data_csv(file:str):  
    col_name = Path(file).name
    
    new_collection = db[col_name]

    
    df = pd.read_csv(file)

    # drop unused column 
    if "Unnamed: 11" in df.columns:
        df = df.drop("Unnamed: 11", axis=1)

    # convert data types
    df = df.convert_dtypes()
    df['Date'] = pd.to_datetime(df['Date'])
    # df['Total volume'] = pd.to_numeric()
   
   # fill NA in Average price column
    fill_average_s = average_price(df['High price'], df['Low price'])
    df['Average price'] = df['Average price'].fillna(fill_average_s)
    # forward fill all dates that do not have any data
    df['Average price'] = df['Average price'].ffill()

    # set opening price
    df['Opening price'] = df['Opening price'].fillna(0)
    opening_s = df['Opening price']
    # zeros = np.zeros(shape=(opening_s.size))
    # zeros_s = Series(zeros)
    df['Opening price'].loc[opening_s == 0] = df['Average price']

    # Forward fill turnover
    df['Turnover'] = df['Turnover'].ffill()

    # check total_volume
    fill_volume_s = total_volume(df['Turnover'], df['Average price'])
    df['Total volume'] = df['Total volume'].fillna(fill_volume_s)
    # set all NaN equal to 0

    # fill missing bid and ask price with average price
    df['Bid'] = df["Bid"].fillna(fill_average_s)
    df['Ask'] = df["Ask"].fillna(fill_average_s)



    data = df.to_dict(orient="records")
    new_collection.insert_many(data)
    
    if (new_collection.count_documents({}) > 0):
        print(f"{col_name} imported to MongoDB successfully.")
    else:
        print("Something went wrong!")


def average_price(high_price: Series, low_price: Series):
    return high_price.add(low_price).multiply(0.5)


def total_volume(turnover: Series, average: Series):
    return turnover.div(average).astype('int64')


def collection_exists(col_name:str) -> bool:
    collection_names = db.list_collection_names()
    if any(col_name == c for c in collection_names):
        print(col_name + " - Exists in DB!")
        return True
    return False

    
def load_all_new_csv(path: str):
    csv_files = os.listdir(path)
    for csv_file in csv_files:
        if not collection_exists(csv_file):
            file = os.path.join(path, csv_file)
            load_market_data_csv(file)

def load_assets_csv(file:str):  
    col_name = Path(file).name
    new_collection = db[col_name]


    df = pd.read_csv(file)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    data = df.to_dict(orient="records")
    new_collection.insert_many(data)
    
    if (new_collection.count_documents({}) > 0):
        print("CSV data imported to MongoDB successfully.")
    else:
        print("Something went wrong!")
            

def load_sources_csv(file:str):  
    col_name = Path(file).name
    new_collection = db[col_name]

    df = pd.read_csv(file)
    data = df.to_dict(orient="records")
    new_collection.insert_many(data)

    
    if (new_collection.count_documents({}) > 0):
        print("CSV data imported to MongoDB successfully.")
    else:
        print("Something went wrong!")


def stock_price_return(col_name: str):
    col = db[col_name]
    pipeline = [
            { "$sort": { "Date": 1 }},
            { "$limit": 1}
    ]

    data_1 = list(col.aggregate(pipeline))
    price_1 = data_1[0]["Average price"]

    pipeline = [
        { "$sort": { "Date": -1 }},
        { "$limit": 1}
    ]

    data_2 = list(col.aggregate(pipeline))
    price_2 = data_2[0]["Average price"]

    return (price_2 - price_1) / price_1

def drop_collection(col_name: str):
    db[col_name].drop()

# def get_all_market_data_collections():
#     col = db['tbl_market_data.csv']
#     names = col.find({}, {"_id": False}) 
#     return list(names)

def get_all_tbl_collections():
    filter = {"name": {"$regex": r"tbl\w+.csv"}}
    return db.list_collection_names(filter=filter)

def get_all_market_data_collections():
    filter = {"name": {"$regex": r"\w*-*((\w)*)-\d+-\d+-\d+-\d+-\d+-\d+.csv"}}
    return db.list_collection_names(filter=filter)

def drop_all_market_data_collections():
    gen = (c for c in get_all_market_data_collections())
    while True:
        try:
            col_name = next(gen)
            print("Drop " + col_name)
            drop_collection(col_name)
        except StopIteration:
            break




