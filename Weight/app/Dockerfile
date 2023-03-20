FROM python:3.8-alpine

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install flask
RUN pip install mysql.connector.python

COPY . . 

CMD ["python3", "app.py"]