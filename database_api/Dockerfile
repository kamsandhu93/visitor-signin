FROM python:3.7-alpine

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG WORK_DIR=/databaseapi

ENV DB_PATH $WORK_DIR/database
ENV LOG_PATH $WORK_DIR/log/database_api.log

COPY /requirements.txt $WORK_DIR/requirements.txt

RUN apk -q update && apk -q upgrade \
 && apk -q add curl \
 && apk -q add bash \
 && apk -q add bash-completion \
 && pip install -qr $WORK_DIR/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #create work directory
 && mkdir $WORK_DIR/log \
 && mkdir $WORK_DIR/database

COPY . $WORK_DIR/.

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE $PORT

CMD ["python3", "main.py"]
