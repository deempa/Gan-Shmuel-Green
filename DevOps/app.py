from flask import Flask, request, Response, render_template
import os
import requests
import subprocess
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, static_url_path='/static' )

#user_dict = {"AvihaiZiv": "avihai40@gmail.com", "OfirAviv": "ofir851@gmail.com"}

# devops_mails = ["masrab11@gmail.com", "Michal.dikun13@gmail.com", "theoneandonlypeleg@gmail.com"]

devops_mails = ["masrab11@gmail.com"]

@app.route("/trigger", methods=["GET", "POST"])
def trigger():
    if request.method == "POST":
        if 'X-GitHub-Event' in request.headers and request.headers['X-GitHub-Event'] == 'push':                
            data = request.get_json()
            branch_name = data['ref'].split('/')[-1]
            repo_url = data['repository']['clone_url']
            repo_name = data['repository']['name']    
            # pusher = data['pusher']['name']
            committer_email = data['commits'][0]['committer']['email']
              
            # Delete Cloned Repo If Exists.
            try:
                os.system(f"rm -rf ./{repo_name}")
            except:
                pass     
                   
            if branch_name == "main":
                result = subprocess.run(['bash', './scripts/build.sh', repo_name, repo_url]) 
                if result.returncode == 0:
                    subprocess.run(['bash', './scripts/terminatetest.sh']) 
                    print("Deployed to production.")
                    # send_email(committer_email, "CI / CD Success.", "Everything is good with your commit.")  
                    for mail in devops_mails:
                        send_email(mail, "CI / CD Success.", f"Merge to branch {branch_name} was success.\nIt passed all the tests.\n Deployed to Production.")  
                else:
                    subprocess.run(['bash', './scripts/terminatetest.sh']) 
                    # send_email(committer_email, "CI / CD Failed.", "Something broke with your commit.")  
                    for mail in devops_mails:
                       send_email(mail, "CI / CD Failed.", f"Merge to branch {branch_name} was failed.\nIt unpassed all the tests\nPlease revert to the last commit of {branch_name} branch.")           
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

@app.route('/monitoring')
def index():
    # Check status of services
    billing_status = check_server_status("http://3.76.109.165:8082/health")
    weight_status = check_server_status("http://3.76.109.165:8083/health")
    # Render HTML template with status information
    return render_template('index.html', billing_status=billing_status, weight_status=weight_status)

def check_server_status(service_url):
    try:
        response = requests.get(service_url)
        print("CONTENT: ", response.text)
        if response.status_code == 200:
            return 'active'
        elif response.status_code == 503:
            return 'db_inactive'
    except:
        return 'inactive'


@app.route("/health", methods=["GET"])
def health():
    return Response("ok", status=200)
            
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)