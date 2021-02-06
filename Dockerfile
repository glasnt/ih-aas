FROM python:3.9-slim

ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME

COPY . . 

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
