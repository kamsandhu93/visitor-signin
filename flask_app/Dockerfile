FROM python:3.7-alpine

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG DB_FILE
ARG WRK_DIR=/databaseservice

ENV DB_PATH /app/visitor_app/database/$DB_FILE
ENV PORT 5000
ENV HOST 0.0.0.0
ENV LOG_PATH /app/visitor_app/log/visitor_app.log

COPY requirements.txt /tmp/

RUN apk update && apk upgrade \
 && apk add curl \
 #install python packages
 && pip install -r /tmp/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #create work directory
 && mkdir app/visitor_app/log \
 && mkdir app/visitor_app/database

ADD ./visitor_app /app/visitor_app
ADD ./main.py /app/


WORKDIR /app

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE $PORT
CMD ["python3", "main.py"]
