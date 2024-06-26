# import app.app as app
from app.import_csv import import_csv
from app.database import mongo_manager
from pathlib import Path
import os

def test_get_three_source_file_names():
    source_file_names = [
        "8TRA-2019-06-28-2024-04-30.csv",
        "ABB-1999-06-22-2024-04-30.csv",
        "ALFA-2002-05-17-2024-04-30.csv"
        ]
    base_dir = Path(__file__).parent.parent.absolute()
    print(base_dir)
    path = str(base_dir) + "/data/"
    print(path)
    csv_files = import_csv.get_source_files(path)
    res = all(f in csv_files for f in source_file_names)

    assert res == True

# def all_market_data_collections():
    
#     for c in cols:
#         yield c['collection_name']

def test_all_market_data_collections():
    cols = [{'collection_name': 'a'},{'collection_name': 'b'}, {'collection_name': 'c'}]
    gen = (c['collection_name'] for c in cols)
    name1 = next(gen)
    print(name1)
    name2 = next(gen)
    print(name2)
    name3 = next(gen)
    print(name3)
    assert name1 == 'a' and name2 == 'b' and name3 == 'c'


def test_get_one():
    col_name = '8TRA-2019-06-28-2024-04-30.csv'
    res = mongo_manager.get_one(col_name)
    print("test_get: " + str(res))
    assert res["_id"] != ""

def test_get_all():
    col_name = '8TRA-2019-06-28-2024-04-30.csv'
    res = mongo_manager.get_all(col_name)
    print("test_get: " + str(res))
    assert res is not None        

def test_get_all_market_data_collections():
    collection_names = mongo_manager.get_all_market_data_collections()
    for c in collection_names:
        print(c)
    assert len(collection_names) == 41

def test_get_all_tbl_collections():
    collection_names = mongo_manager.get_all_tbl_collections()
    for c in collection_names:
        print(c)
    assert len(collection_names) == 2






