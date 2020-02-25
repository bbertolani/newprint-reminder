import datetime
import json
import os
import time
import urllib

from bson.json_util import dumps
from models.reminder import Reminder


def getReminder():
    obj = Reminder.objects.all()
    result = obj.only("order", "part").values()
    return dumps(result)


def postReminder(request):
    order = str(request.get("order"))
    force = request.get("force")
    notification = str(request.get("notification"))
    part = str(request.get("part"))
    email = request.get("email")
    url = request.get("url")
    status = request.get("status")
    insert = False

    try:
        Reminder.objects.get({"order": order, "part": part})
        obj = {
            "msg": "Order already waiting approval",
            "order": order,
            "part": part,
            "notification": notification,
        }
        if force:
            Reminder.objects.get({"order": str(order)}).delete()
            insert = True
    except Reminder.DoesNotExist:
        insert = True

    if insert == True:
        Reminder(
            order,
            part,
            email,
            url,
            status,
            notification,
            createdAt=datetime.datetime.now(),
        ).save()
        obj = {
            "order": order,
            "part": part,
            "msg": "Order is now waiting approval, First Notification",
        }

    return dumps(obj)


def putInfo(order, request):
    part = str(request.get("part"))
    status = request.get("status") or "None"
    notification = request.get("notification") or "None"

    try:
        orderReminder = Reminder.objects.raw({"order": order, "part": part})
        if status != "None":
            orderReminder.update({"$set": {"status": status}})
        if notification != "None":
            orderReminder.update({"$set": {"notification": notification}})
        msg = {"msg": "Order Update", "order": order, "part": part}
    except Reminder.DoesNotExist:
        msg = {"msg": "Order not found", "order": order, "part": part}

    return msg


def getInfo(order, request):
    try:
        part = str(request.get("part"))
        obj = Reminder.objects.get({"order": order, "part": part})
        msg = dumps(obj.to_son().to_dict())
    except Reminder.DoesNotExist:
        msg = {"order": order, "part": part, "msg": "Order not found"}

    return msg
