import sys
import os

from config.mongo import initMongo
from flask import Flask, request
from scripts.scripts import postReminder, getReminder, putInfo, getInfo
from scripts.trigger import triggerReminder

if os.environ.get('ENV') == "DEV":
    try:
        import ptvsd

        ptvsd.enable_attach(address=("0.0.0.0", 5050))
        print("ptvsd is started")
        ptvsd.wait_for_attach()

    except:
        print("Failed or running....")

app = Flask(__name__)


@app.route("/api/reminder", methods=["GET", "POST"])
def methodsReminder():
    if request.method == "GET":
        return getReminder()
    if request.method == "POST":
        return postReminder(request.get_json())


@app.route("/api/reminder/<order_number>/<order_ID>", methods=["GET", "PUT"])
def methodsInfo(order_number, order_ID):
    if request.method == "GET":
        return getInfo(order_number, order_ID, request.get_json())
    if request.method == "PUT":
        return putInfo(order_number, order_ID, request.get_json())


@app.route("/api/triggerRemider", methods=["GET"])
def methodsTrigger():
    return triggerReminder()


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8080, debug=False)
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
