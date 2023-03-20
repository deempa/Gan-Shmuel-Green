from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route("/payload", methods=["GET", "POST"])
def payload():
    if request.method == "POST":
        if 'X-GitHub-Event' in request.headers and request.headers['X-GitHub-Event'] == 'push':                
            data = request.get_json()
            branch_name = data['ref'].split('/')[-1]
            repo_url = data['repository']['clone_url']
            repo_name = data['repository']['name']
            
            # Clone and checkout to the branch that push
            os.mkdir("./Cloned")
            os.chdir("./Cloned")       
            print(os.getcwd())
            # subprocess.run(['git', 'clone', repo_url])
            # os.chdir("./" + repo_name)
            # subprocess.run(['git', 'checkout', branch_name])
            
            return f"{branch_name}, {repo_url}, {repo_name}"
            

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081)