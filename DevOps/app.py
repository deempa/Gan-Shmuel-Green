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
            
            clone(repo_url)
            
            # Build for Weight
            path_weight_dockerfile_app = f"{repo_name}/Weight/app/"
            path_weight_dockerfile_db = f"{repo_name}/Weight/schemas/"
            build(path_weight_dockerfile_db, "weight_db")
            build(path_weight_dockerfile_app, "weight_app")          
            # Build for Billing
        
            path_billing_dockerfile_app = f"{repo_name}/Billing/"
            build(path_billing_dockerfile_app, "billing_app")


def clone(repo_url, repo_name):
    Repo.clone_from(repo_url, f"./{repo_name}/")
    
def build(dockerfile_path, image_name):
    client.images.build(path=dockerfile_path, tag=image_name)
    
# def run(branch_name):
#     lower_branch_name = branch_name.lower()
#     client.containers.run(f"{lower_branch_name}_image", detach=True, hostname=f"{branch_name}_app", ports={'8082': '5000'})
 
def mailing_Feature():
    pass

        
@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)