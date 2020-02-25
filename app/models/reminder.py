from pymodm import MongoModel, fields

from config.mongo import initMongo

initMongo()

class Reminder(MongoModel):
  order = fields.CharField()
  part = fields.CharField()
  email = fields.EmailField()
  url = fields.CharField()
  notification = fields.CharField()
  status = fields.CharField()
  createdAt = fields.DateTimeField()
