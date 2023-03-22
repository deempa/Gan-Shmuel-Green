from flask import Flask
import requests

app = Flask(__name__)

#GET /unknown (called by admin)
#GET /weight (report by time)
#GET /item/<id> (truck/container report)
#GET /session/<id> (weighing report)
#GET /health

@app.route('/health')
def healthcheck():
    
    try:
        u = requests.get('localhost:5000/unknown')
        if u.status_code == 200:
            return(f"{u}: Is Healthy. status code: 200")
    except:
            return(f"{u}: Could Not Connect To The Database. status code: 500")


    try:
        w = requests.get('localhost:5000/weight')
        if w.status_code == 200:
            return(f"{w}: Is Healthy. status code: 200")
    except:
            return(f"{w}: Could Not Connect To The Database. status code: 500")


    try:
        i = requests.get('localhost:5000/item/<id>')
        if i.status_code == 200:
            return(f"{i}: Is Healthy. status code: 200")
    except:
            return(f"{i}: Could Not Connect To The Database. status code: 500")


    try:
        s = requests.get('localhost:5000/session/<id>')
        if s.status_code == 200:
            return(f"{s}: Is Healthy. status code: 200")
    except:
            return(f"{s}: Could Not Connect To The Database. status code: 500")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)