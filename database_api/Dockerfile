FROM python:3.7-alpine

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG WORK_DIR=/home/databaseapi

ENV DB_PATH /home/database
ENV LOG_PATH /home/log/database_api.log

COPY /database_api/requirements.txt $WORK_DIR/requirements.txt

RUN apk -q update && apk -q upgrade \
 && apk -q add curl \
 && apk -q add bash \
 && apk -q add bash-completion \

 && pip install -qr $WORK_DIR/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #create work directory
 && mkdir /home/log \
 && mkdir /home/database

COPY /shared $WORK_DIR/shared/
COPY /database_api $WORK_DIR/

ENV PYTHONPATH "${PYTHONPATH}:/home"
WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE $PORT

CMD ["python3", "main.py"]
