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
            
            subprocess.run(['git', 'clone', repo_url])
            
            if branch_name == "Billing":
                os.chdir(f"./{repo_name}/")
                subprocess.run(['git', 'checkout', branch_name])
                os.chdir(f"./{branch_name}/")
                docker_billing_build_command = "docker build -t billing_image ."
                os.system(docker_billing_build_command)
                docker_billing_run_command = "docker run -d --name billing_app -p 8082:5000 billing_image"
                os.system(docker_billing_run_command)
                os.chdir("../../")
                      
            return f"{branch_name}, {repo_url}, {repo_name}"
            
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081)