import datetime
import json
import os
import time
import urllib

from bson.json_util import dumps
from models.reminder import Reminder


def getStatus():
    status = {"0": "Waiting Approval", "1": "Approved", "2": "Disapproved"}
    return dumps(status)


def getList():
    obj = Reminder.objects.raw({"status": 0})
    result = obj.values()
    return result


def getReminder():
    obj = Reminder.objects.all()
    result = obj.only("order_number", "order_ID", "item_ID").values()
    return dumps(result)


def postReminder(request):
    origin = request.get("origin")
    order_number = str(request.get("order_number"))
    order_ID = str(request.get("order_ID"))
    item_ID = str(request.get("item_ID")) or "0"
    email = request.get("email")
    product_desc = request.get("product_desc")
    project_title = request.get("project_title")
    url = request.get("url")
    status = request.get("status")
    force = str(request.get("force"))
    insert = False
    notification = 1

    try:
        obj = Reminder.objects.get(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        )
        msg = {
            "msg": "Order already waiting approval",
            "order_number": obj.order_number,
            "order_ID": obj.order_ID,
            "item_ID": obj.item_ID,
            "notification": obj.notification,
        }
        if force == "1" or obj.status == 2:
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
    item_ID = str(request.get("item_ID")) or None
    status = request.get("status") or None

    try:
        orderReminder = Reminder.objects.raw(
            {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
        )
        if status == 1:
            orderReminder.update({"$set": {"status": status}})
            msg = {
                "msg": "Order Approved",
                "order_number": order_number,
                "order_ID": order_ID,
                "item_ID": item_ID,
            }
            Reminder.objects.raw(
                {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
            ).delete()
        else:
            obj = Reminder.objects.get(
                {"order_number": order_number, "order_ID": order_ID, "item_ID": item_ID}
            )
            calcNotification = obj.notification + 1
            orderReminder.update({"$set": {"notification": calcNotification}})
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
