FROM python:3.7-alpine
LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG DB_FILE

ARG WORK_DIR=/databaseadmin
ARG DB_PATH=$WORK_DIR/database/$DB_FILE
ARG START_SCRIPT=$WORK_DIR/start.sh
ARG PORT=5001
ARG HOST=0.0.0.0

COPY requirements.txt /tmp/

RUN apk -q update && apk -q upgrade \
 && apk -q add curl \
 #install python packages
 && pip install -qr /tmp/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #make work directory
 && mkdir $WORK_DIR \
 && mkdir $WORK_DIR/log \
 && mkdir $WORK_DIR/database \
 #make start script
 && touch $START_SCRIPT \
 && echo "#!/bin/sh" >> $START_SCRIPT \
 && echo sqlite_web -H $HOST -p $PORT $DB_PATH >> $START_SCRIPT \
 && chmod +x $START_SCRIPT

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT || exit 1

EXPOSE $PORT
CMD ["/bin/sh", "start.sh"]
