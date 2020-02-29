import sys

from config.mongo import initMongo
from flask import Flask, request
from scripts.scripts import postReminder, getReminder, putInfo, getInfo
from scripts.trigger import triggerReminder

app = Flask(__name__)

@app.route('/api/reminder', methods=['GET', 'POST', 'PUT'])
def methodsReminder():
  if request.method == 'GET':
    return getReminder()
  if request.method == 'POST':
    return postReminder(request.get_json())

@app.route('/api/reminder/<order>', methods=['GET', 'PUT'])
def methodsInfo(order):
  if request.method == 'GET':
    return getInfo(order, request.get_json())
  if request.method == 'PUT':
    return putInfo(order, request.get_json())

@app.route('/api/triggerRemider', methods=['GET'])
def methodsTrigger():
  return triggerReminder()
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
