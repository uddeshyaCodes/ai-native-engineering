import requests
from flask import Flask, request, redirect, render_template

app= Flask(__name__)

API = "http://localhost:5000"


# keep task ids for polling
task_ids=[]
statuses={}

@app.route("/")
def index():
    for tid in task_ids:
        statuses[tid]=requests.get(f'{API}/task/{tid}').json()

    tasks= [(tid, statuses[tid]['status'], statuses[tid]['result']) for tid in task_ids]  
    return render_template('index.html', tasks =tasks)  


@app.route("/submit", methods=['POST'])
def submit():
    n1=float(request.form['number1'])
    n2=float(request.form['number2'])
    
    res = requests.post(f'{API}/task', json={"number1": n1, "number2": n2})

    data=res.json()
    task_ids.append(data["task_id"])
    statuses[data["task_id"]]= data

    return redirect("/")




if __name__== "__main__":
    app.run(port=5001, debug= True)
