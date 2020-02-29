from pymodm import MongoModel, fields

from config.mongo import initMongo

initMongo()


class Reminder(MongoModel):
    origin = fields.CharField(required=True)
    order_number = fields.IntegerField(required=True)
    order_ID = fields.CharField(required=True)
    item_ID = fields.IntegerField(blank=True)
    email = fields.EmailField(required=True)
    product_desc = fields.CharField(blank=True)
    project_title = fields.CharField(blank=True)
    url = fields.CharField(required=True)
    notification = fields.IntegerField(required=True, choices=[0, 1, 2, 3])
    status = fields.IntegerField(required=True, choices=[0, 1, 2, 3])
    createdAt = fields.DateTimeField(required=True)
