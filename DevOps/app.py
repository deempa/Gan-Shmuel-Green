from flask import Flask, request, Response
import docker
from git import Repo
import os
import subprocess
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

client = docker.from_env()

branches = ("main", "Billing", "Weight")

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
            
            # ci test env
            # if branch_name in branches:
            #     subprocess.call(['bash', './scripts/ci_test_env.sh', repo_name, repo_url, branch_name])      
                   
            if branch_name == "main":
                result = subprocess.run(['bash', './scripts/build.sh', repo_name, repo_url])  
                if result.returncode == 0:
                    print("Build to prod succeded")
                    send_email("Build successed!", "the build and test succeded", "masrab11@gmail.com")
                else:
                    print("Build to prod Failed")         
                    send_email("Build failed!", "the build and test Failed", "masrab11@gmail.com")           
            return "ok"
            
            
def send_email(subject, message, to_mail):
    # Set up the connection to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('ganshmuelgreen@gmail.com', 'ganshmuel13!')

    # Create the message and set the recipient
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'ganshmuelgreen@gmail.com'
    msg['To'] = to_mail

    # Send the email
    server.sendmail('ganshmuelgreen@gmail.com', to_mail, msg.as_string())
    server.quit()

        
@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)