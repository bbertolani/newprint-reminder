# from pymongo import MongoClient
import sys

from pymodm import connect


def initMongo():
    try:
        mong = "mongodb://mongo_db:27017/newprint"
        client = connect(mong)
    except:
        print("Mongo failed")
        sys.exit(1)

    return client
