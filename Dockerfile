FROM python:3.7-alpine

ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME


# For Pillow
RUN apk add --update build-base jpeg-dev zlib-dev 
RUN apk add --update git

COPY . . 

RUN pip install -r requirements.txt
RUN pip freeze

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
