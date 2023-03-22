from flask import Flask
import requests

app = Flask(__name__)

health_status = True

@app.route('/unknown')
def healthcheck():
    url = '   '
    get = requests.get({url})
    if health_status == 200:
        return(f"{url}: is healthy. status code: 200")
    else:
        return(f"{url}: is not healthy. status code: 500")


@app.route('/weight')
def healthcheck():
    url = '  '
    get = requests.get({url})
    if health_status == 200:
        return(f"{url}: is healthy. status code: 200")
    else:
        return(f"{url}: is not healthy. status code: 500")


@app.route('/item')
def healthcheck():
    url = '  '
    get = requests.get({url})
    if health_status == 200:
        return(f"{url}: is healthy. status code: 200")
    else:
        return(f"{url}: is not healthy. status code: 500")


@app.route('/session')
def healthcheck():
    url = '  '
    get = requests.get({url})
    if health_status == 200:
        return(f"{url}: is healthy. status code: 200")
    else:
        return(f"{url}: is not healthy. status code: 500")


@app.route('/health')
def healthcheck():
    url = 'localhost:5000/weight'
    get = requests.get({url})
    if health_status == 200:
        return(f"{url}: is healthy. status code: 200")
    else:
        return(f"{url}: is not healthy. status code: 500")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)