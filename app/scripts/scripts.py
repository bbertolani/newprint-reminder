import datetime
import json
import os
import time
import urllib

from bson.json_util import dumps
from models.reminder import Reminder


def getReminder():
    obj = Reminder.objects.all()
    result = obj.only("order_number", "order_ID", "item_ID").values()
    return dumps(result)


def postReminder(request):
    origin = request.get("origin")
    order_number = str(request.get("order_number"))
    order_ID = str(request.get("order_ID"))
    item_ID = str(request.get("item_ID")) or '0'
    email = request.get("email")
    product_desc = request.get("product_desc")
    project_title = request.get("project_title")
    url = request.get("url")
    notification = request.get("notification")
    status = request.get("status")
    force = request.get("force")
    insert = False

    try:
        Reminder.objects.get(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        )
        msg = {
            "msg": "Order already waiting approval",
            "order_number": order_number,
            "order_ID": order_ID,
            "item_ID": item_ID,
            "notification": notification,
        }
        if force == 1:
            Reminder.objects.get(
                {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
            ).delete()
            insert = True
    except Reminder.MultipleObjectsReturned:
        Reminder.objects.raw(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        ).delete()
        insert = True
    except Reminder.DoesNotExist:
        insert = True

    if insert == True:
        try:
            Reminder(
                origin,
                order_number,
                order_ID,
                item_ID,
                email,
                product_desc,
                project_title,
                url,
                notification,
                status,
                createdAt=datetime.datetime.now(),
            ).save()
            msg = {
                "order_number": order_number,
                "order_ID": order_ID,
                "item_ID": item_ID,
                "msg": "Order is now waiting approval, First Notification",
            }
        except:
            msg = {
                "order_number": order_number,
                "order_ID": order_ID,
                "item_ID": item_ID,
                "msg": "Order Failed",
            }

    return dumps(msg)


def putInfo(order_number, order_ID, request):
    order_number = str(order_number)
    order_ID = str(order_ID)
    item_ID = str(request.get("item_ID"))
    notification = request.get("notification")
    status = request.get("status")

    try:
        orderReminder = Reminder.objects.raw(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        )
        if status != "None":
            orderReminder.update({"$set": {"status": status}})
        if notification != "None":
            orderReminder.update({"$set": {"notification": notification}})
        msg = {
            "msg": "Order Update",
            "order_number": order_number,
            "order_ID": order_ID,
            "item_ID": item_ID,
        }
    except Reminder.DoesNotExist:
        msg = {
            "msg": "Order not found",
            "order_number": order_number,
            "order_ID": order_ID,
            "item_ID": item_ID,
        }

    return msg


def getInfo(order_number, order_ID, request):
    item_ID = str(request.get("item_ID"))
    try:
        obj = Reminder.objects.get(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        )
        msg = dumps(obj.to_son().to_dict())
    except Reminder.DoesNotExist:
        msg = {
            "order_number": order_number,
            "order_ID": order_ID,
            "item_ID": item_ID,
            "msg": "Order not found",
        }

    return msg
