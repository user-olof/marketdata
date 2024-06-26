
from pymongo import MongoClient
from pymongo.database import Database
# import logging


MONGODB_URI = "mongodb://192.168.0.204:27017/"

client = MongoClient(MONGODB_URI)
db = client["marketdata"]


# class MongoManager:
#     client: MongoClient = None
#     db: Database = None

#     def connect_to_database(self, uri: str):
#         logging.info("Connecting to MongoDB...")
#         self.client = MongoClient(uri)
#         self.db = self.client.main_db
#         logging.info("Connected to MongoDB.")

#     def close_database_connection(self):
#         logging.info("Closing connection with MongoDB.")
#         self.client.close()
#         logging.info("Closed connection with MongoDB.")