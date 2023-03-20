FROM thesoul/ubuntu-dind:docker-18.09.7

RUN apt update -y && \
    apt install -y python3.8 python3-pip

WORKDIR /devopsapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]