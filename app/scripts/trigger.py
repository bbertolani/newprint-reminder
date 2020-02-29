import datetime
import json
import os
import time
import urllib

import requests

from bson.json_util import dumps
from models.reminder import Reminder


def triggerReminder():
    obj = Reminder.objects.raw({"status": 1})
    result = obj.values()

    SWITCH_URL = "http://192.168.0.144:51080/test"

    for order in list(result):
        msg = "INIT Order:{} Part:{} - {}".format(
            order["order_number"], order["order_ID"], datetime.datetime.now()
        )
        print(msg)
        xml = '<?xml version="1.0" encoding="UTF-8"?><job>'

        if order["origin"] == "Offline":
            xml += "<origin>{}</origin>".format(order["origin"])
            xml += "<order_number>{}</order_number>".format(order["order_number"])
            xml += "<order_ID>{}</order_ID>".format(order["order_ID"])
            xml += "<email>{}</email>".format(order["email"])
            xml += "<product_desc>{}</product_desc>".format(order["product_desc"])
            xml += "<url>{}</url>".format(order["url"])
        else:
            xml += "<origin>{}</origin>".format(order["origin"])
            xml += "<order_number>{}</order_number>".format(order["order_number"])
            xml += "<order_ID>{}</order_ID>".format(order["order_ID"])
            xml += "<item_ID>{}</item_ID>".format(order["item_ID"])
            xml += "<email>{}</email>".format(order["email"])
            xml += "<product_desc>{}</product_desc>".format(order["product_desc"])
            xml += "<project_title>{}</project_title>".format(order["project_title"])
            xml += "<url>{}</url>".format(order["url"])

        xml += "</job>"

        try:
            requests.post(
                SWITCH_URL, data=xml, headers={"Content-Type": "application/xml"}
            )
        except:
            print("Link not available")
    return dumps(result)
