import pymongo

from configs import MONGO_DB_URI, MONGO_DB_NAME

class db(object):
    name = MONGO_DB_NAME
    uri = MONGO_DB_URI

    @staticmethod
    def init():
        client = pymongo.MongoClient(db.uri)
        db.DATABASE = client[db.name]

    @staticmethod
    def insert(collection, data):
        db.DATABASE[collection].insert(data)

    def insert_one(collection, data):
        return db.DATABASE[collection].insert_one(data)

    @staticmethod
    def find_one(collection, query):
        return db.DATABASE[collection].find_one(query)

    def find(collection, query):
        return db.DATABASE[collection].find(query)

    def find_and_modify(collection, query, **kwargs):
        print(kwargs)
        db.DATABASE[collection].find_and_modify(query=query,
                                                update={"$set": kwargs}, upsert=False,
                                                full_response=True)
