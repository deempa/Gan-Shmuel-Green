from flask import Flask, request, Response, render_template
import docker
from git import Repo
import os
import requests
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
                   
            if branch_name == "main":
                result = subprocess.run(['bash', './scripts/build.sh', repo_name, repo_url]) 
                if result.returncode == 0:
                    print("Deployed to production.")
                    
                else:
                    print("Something in ci got wrong. ")
                    send_email(com)            
            return "ok"
            
            
def send_email(recipient, subject, message):
    # Set up the connection to the Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
 #setting up the email env + app_pswd
    email = 'ganshmuelgreen@gmail.com'
    password = "lbpncwxiuyolntwp"
    server.login(email, password)

    # Create the message and set the recipient
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = recipient
    
     # Send the email
    server.sendmail(email, recipient, msg.as_string())
    server.quit()

    return 'Email sent successfully!'
    

@app.route("/monitoring", methods=["GET"])
def monitor():
    res = requests.get('http://3.76.109.165:8081/health')
    code = res.status_code
    if res:
        status = "active"
    else:    
        status = "inactive"
    return render_template('index.html', code=code, status=status)


@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)