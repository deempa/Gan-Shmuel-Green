FROM python:3.10

WORKDIR /devopsapp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]