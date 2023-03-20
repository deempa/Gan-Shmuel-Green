FROM python:3.10

RUN apt-get update -y

RUN apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

WORKDIR /devopsapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]