FROM docker:dind

ENV DOCKER_HOST=unix:///var/run/docker.sock

RUN apk update && \
    apk add --no-cache curl python3 py3-pip && \
    pip3 install docker-compose && \
    curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh

WORKDIR /devopsapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]