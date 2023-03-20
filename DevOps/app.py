from flask import Flask, request, Response
import docker
from git import Repo

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
            
            # subprocess.run(['git', 'clone', repo_url])
            
            # if branch_name == "main":
            #     os.chdir(f"./{repo_name}/")
            #     subprocess.run(['git', 'checkout', branch_name])
            #     os.chdir(f"./{branch_name}/")
            #     # docker_billing_build_command = "docker build -t billing_image ."
            #     client.images.build(".")
            #     os.system(docker_billing_build_command)
            #     docker_billing_run_command = "docker run -d --name billing_app -p 8082:5000 billing_image"
            #     os.system(docker_billing_run_command)
            #     os.chdir("../../")
            
            if branch_name == "main":
                Repo.clone_from(repo_url, "./Gan-Shmuel-Green")
                client.images.build("./Gan-Shmuel-Green/Billing/", tag="billing_image")
                client.containers.run("billing_image", detach=True, hostname="billing_app", ports={'8082': '5000'})
                
                      
            return f"{branch_name}, {repo_url}, {repo_name}"
        
        
@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081)