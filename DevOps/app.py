from flask import Flask, request

app = Flask(__name__)

@app.route("/payload", methods=["GET", "POST"])
def payload():
    if request.method == "POST":
        data = request.get_json()
        return 'success'

if __name__ == "__main__":
    app.run(port=8081)