FROM python:3.6-alpine
MAINTAINER NHS Digital Delivery Centre,  Team-Grads

ARG BRANCH
ARG DB_FILE

ARG WORK_DIR=/visitor-db
ARG DB_PATH=$WORK_DIR/database/$DB_FILE
ARG START_SCRIPT=$WORK_DIR/start.sh
ARG APP_PORT=5001
ARG APP_HOST=0.0.0.0

RUN apk update && apk upgrade \
 && apk add curl \
 && rm -rf /var/cache/apk/*

RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN touch $START_SCRIPT
RUN echo #!/bin/sh >> $START_SCRIPT
RUN echo sqlite_web -H $APP_HOST -p $APP_PORT $DB_PATH >> $START_SCRIPT
RUN chmod +x $START_SCRIPT

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$APP_HOST:$APP_PORT || exit 1

EXPOSE $APP_PORT
CMD ["/bin/sh", "start.sh"]
