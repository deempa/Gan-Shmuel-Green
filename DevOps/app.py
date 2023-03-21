from flask import Flask, request, Response
import docker
from git import Repo
import os
import subprocess


app = Flask(__name__)

client = docker.from_env()

@app.route("/trigger", methods=["GET", "POST"])
def trigger():
    if request.method == "POST":
        if 'X-GitHub-Event' in request.headers and request.headers['X-GitHub-Event'] == 'push':                
            data = request.get_json()
            branch_name = data['ref'].split('/')[-1]
            repo_url = data['repository']['clone_url']
            repo_name = data['repository']['name']    
            pusher = data['pusher']['name']
            committer_email = data['commits'][0]['committer']['email']
              
            # Delete Cloned Repo If Exists.
            try:
                os.system(f"rm -rf ./{repo_name}")
            except:
                pass
            
            clone(repo_url, repo_name) 
                               
            # build(repo_name, branch_name)   
            
            print("Docker compose up.")
            subprocess.call(['./docker-compose.sh'])
                    
            # tests          
            print("testing..... Completed")
            
            # print("Running...")
            # run(branch_name)
              
            return "OK", 200
        
def clone(repo_url, repo_name):
    Repo.clone_from(repo_url, f"./{repo_name}")
    
def build(repo_name, branch_name):
    lower_branch_name = branch_name.lower()
    client.images.build(path=f"./{repo_name}/{branch_name}/", tag=f"{lower_branch_name}_image")
    
def run(branch_name):
    lower_branch_name = branch_name.lower()
    client.containers.run(f"{lower_branch_name}_image", detach=True, hostname=f"{branch_name}_app", ports={'8082': '5000'})
 
def mailing_Feature():
    pass

        
@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)