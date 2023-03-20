from flask import Flask, request

app = Flask(__name__)

@app.route("/payload", methods=["GET", "POST"])
def payload():
    if request.method == "POST":
        if 'X-GitHub-Event' in request.headers and request.headers['X-GitHub-Event'] == 'push':                
            data = request.get_json()
            return 'success'

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081)