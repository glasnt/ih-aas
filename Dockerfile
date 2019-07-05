FROM python:3.7-slim-stretch

ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME

# for google-cloud-profiler
RUN apt-get update
RUN apt-get install -y build-essential

COPY . . 

RUN pip install -r requirements.txt
RUN pip freeze

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
