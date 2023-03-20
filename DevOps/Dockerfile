FROM docker:20.10.23-dind

RUN apk update && \
    apk add py3-pip git

WORKDIR /devopsapp

COPY requirements.txt .

RUN pip install --ignore-installed -r requirements.txt

COPY . .

CMD ["python3", "app.py"]   