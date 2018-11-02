FROM python:3.7-alpine

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG DB_FILE
ARG WRK_DIR=/databaseapi

ENV DB_PATH $WRK_DIR/database/$DB_FILE
ENV PORT 5000
ENV HOST 0.0.0.0
ENV LOG_PATH $WRK_DIR/log/database_api.log

COPY requirements.txt /tmp/

RUN apk -q update && apk -q upgrade \
 && apk -q add curl \
 #install python packages
 && pip install -qr /tmp/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #create work directory
 && mkdir $WRK_DIR \
 && mkdir $WRK_DIR/log \
 && mkdir $WRK_DIR/database

COPY ./dbapi $WRK_DIR/dbapi
COPY ./main.py $WRK_DIR/


WORKDIR $WRK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE $PORT
CMD ["python3", "main.py"]
