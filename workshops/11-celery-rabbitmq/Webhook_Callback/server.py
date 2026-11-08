import uuid
import time
import random
import threading
import requests
from flask import Flask, request, jsonify

# create an app with Flask: Client
app=Flask(__name__)

#keep ttrack of task
tasks={}

def process(task_id, n1,n2, callback_url):
    time.sleep(random.randint(5,15))
    try:
        result=n1 / n2
        tasks[task_id]={"status":"SUCCESS","result":result}
    except ZeroDivisionError:
        tasks[task_id]={"status":"FAILD","result":None}  

    time.sleep(2)      

    if callback_url:
        try:
            requests.post(callback_url, json={"task_id": task_id, **tasks[task_id]})

        except requests.RequestException: 
            pass

# Flask this task API pooint and starts running tasks in backgroud
# it is to demonstarte webhook
@app.route("/task", methods=['POST'])
def create_task():
    data=request.get_json()
    # create a json 
    n1=data["number1"]
    n2=data["number2"]
    callback_url=data.get("callback_url")

    # generate task id
    task_id=str(uuid.uuid4())
    tasks[task_id]={"status": "PROCESSING", "result":None}

    # runs process method in background
    # tasks that takes long time
    threading.Thread(target=process, args=(task_id, n1,n2, callback_url)).start()

    # return the response immediatly with HTTP 
    #202 is the HTTP code
    return jsonify({"task_id": task_id, **tasks[task_id]}), 202

# wrote this API to demonstrate polling
# application reppetadly asks at the API end point the task status
@app.route("/task/<task_id>")
def get_task(task_id):
    time.sleep(2)
    task=tasks.get(task_id)

    if not task:
        #return 404 on error
        return jsonify({"error": "Not found"}), 404
    return jsonify(task)


if __name__== '__main__':
    app.run(debug=True)



