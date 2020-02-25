#from pymongo import MongoClient
import sys

from pymodm import connect


def initMongo():
  try:
    client = connect('mongodb://host.docker.internal:27017/newprint')
  except:
    print("Mongo failed")
    sys.exit(1)

  return client
