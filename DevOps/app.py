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

#user_dict = {"AvihaiZiv": "avihai40@gmail.com", "OfirAviv": "ofiraviv@gmail.com"}

devops_mails = ["masrab11@gmail.com", "Michal.dikun13@gmail.com", "theoneandonlypeleg@gmail.com"]


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
                    send_email(committer_email, "CI / CD Success.", "Everything is good with your commit.")  
                    for mail in devops_mails:
                        send_email(mail, "CI / CD Success.", "Everything is good with your commit.")  
                else:
                    print("Something in ci got wrong. ")
                    send_email(committer_email, "CI / CD Failed.", "Something broke with your commit.")  
                    for mail in devops_mails:
                       send_email(mail, "CI / CD Failed.", "Something broke with your commit.")           
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
    
@app.route("/monitoring", methods=["GET"])
def monitor():
    res = requests.get('http://3.76.109.165:8081/health')
    code = res.status_code
    if res:
        status = "active"
    else:    
        status = "inactive"
    return render_template('index.html', code=code, status=status)

@app.route('/monitoring2')
def index():
    # Check status of services
    service1_status = check_service_status('http://localhost:8082/health')
    service2_status = check_service_status('http://localhost:8083/health')

    # Render HTML template with status information
    return render_template('index.html', service1_status=service1_status, service2_status=service2_status)

def check_service_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 'active'
        else:
            return 'inactive'
    except requests.exceptions.RequestException:
        return 'Error'


@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)