import pymongo
import os


class Database:
    _URI = os.environ.get('DB_URI')
    _DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database._URI)
        Database._DATABASE = client.get_default_client()

    @staticmethod
    def insert(collection, data):
        return True if Database._DATABASE[collection].insert(data) else False

    @staticmethod
    def delete(collection, query):
        Database._DATABASE[collection].remove(query)

    @staticmethod
    def find(collection, query):
        return Database._DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database._DATABASE[collection].find_one(query)

    @staticmethod
    def count(collection,query):
        return Database._DATABASE[collection].count(query)

    @staticmethod
    def update(collection,query, data):
        return True if Database._DATABASE[collection].update(query,data,upsert=True) else False
