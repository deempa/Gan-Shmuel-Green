FROM python:3.10-alpine3.17

WORKDIR /app

RUN mkdir -p ./in && mkdir -p ./out

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV TZ="Asia/Jerusalem"

COPY . .

EXPOSE 5000

ENTRYPOINT gunicorn --bind 0.0.0.0:5000 app:app
