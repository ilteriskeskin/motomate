import pymongo


class db(object):
    # user = settings.DB_USER
    # name = settings.DB_NAME
    # pw = settings.DB_PASSWORD
    # URI = "mongodb://%s:%s@heybooster-shard-00-00-yue91.mongodb.net:27017,heybooster-shard-00-01-yue91.mongodb.net:27017,heybooster-shard-00-02-yue91.mongodb.net:27017/test?ssl=true&replicaSet=heybooster-shard-0&authSource=admin&retryWrites=true&w=majority" % (
    #     user, pw)
    name = "main"
    URI = "mongodb://ilteriskeskin:Msaia21322312.@myflask-shard-00-00.raeh0.mongodb.net:27017,myflask-shard-00-01.raeh0.mongodb.net:27017,myflask-shard-00-02.raeh0.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=myFlask-shard-0&authSource=admin&retryWrites=true&w=majority"

    @staticmethod
    def init():
        client = pymongo.MongoClient(db.URI)
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
