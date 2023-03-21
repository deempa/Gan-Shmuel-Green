FROM python:3.10-alpine3.17

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN mkidr -p in

EXPOSE 5000

ENTRYPOINT gunicorn --bind 0.0.0.0:5000 app:app