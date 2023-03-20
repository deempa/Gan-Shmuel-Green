
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    if isconnected == 1:
        return ("The Server Is Healthpy, status 200")
    elif isconnected == 0:
        return ("The Server Is Not Healthpy, status 500")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)