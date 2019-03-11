FROM python:3.7-alpine
LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG WORK_DIR=/databaseadmin

ENV DB_PATH $WORK_DIR/database

COPY . $WORK_DIR/.

RUN apk -q update && apk -q upgrade \
 && apk -q add curl \
 && apk -q add bash \
 && apk -q add bash-completion \
 #install python packages
 && pip install -qr $WORK_DIR/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 #make work directory
 && mkdir $WORK_DIR/log \
 && mkdir $WORK_DIR/database

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD /bin/bash healthcheck.sh

EXPOSE $PORT

CMD sqlite_web -H $HOST -p $PORT "$DB_PATH/$DB_FILE"
