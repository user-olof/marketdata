from pymongo import MongoClient
from pathlib import Path
import csv
from bson import Int64, Decimal128
from datetime import datetime
import pandas as pd
import os

MONGODB_URI = "mongodb://192.168.0.204:27017/"

client = MongoClient(MONGODB_URI)
db = client["marketdata"]

def load_market_data_csv(file:str):  
    col_name = Path(file).name
    new_collection = db[col_name]

    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    data = df.to_dict(orient="records")
    new_collection.insert_many(data)
    
    if (new_collection.count_documents({}) > 0):
        print(f"{col_name} imported to MongoDB successfully.")
    else:
        print("Something went wrong!")

def load_all_new_csv(path: str):
    collection_names = db.list_collection_names()
    csv_files = os.listdir(path)
    for csv_file in csv_files:
        if not any(col_name == csv_file for col_name in collection_names):
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


