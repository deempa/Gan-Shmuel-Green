FROM python:3.9-slim-buster



WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN pip install mysql_connector_python

ENTRYPOINT [ "python3", "db_conn.py" ]