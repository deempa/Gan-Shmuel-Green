from flask import Flask, request

app = Flask(__name__)

@app.route("/payload", methods=["GET", "POST"])
def payload():
    if request.method == "POST":
        return "...."

if __name__ == "__main__":
    app.run()