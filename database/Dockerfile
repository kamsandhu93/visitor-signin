FROM python:2.7-alpine
MAINTAINER NHS Digital

ARG WORK_DIR=/visitor-db
ARG TEMP_DIR=/visitor-db-temp
ARG DB_FILE=visitor_db.db
ARG DB_PATH=$WORK_DIR/database/$DB_FILE
ARG BRANCH
ARG APP_PORT=5001
ARG APP_HOST=0.0.0.0

RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

RUN git clone https://github.com/kamsandhu93/visitor-signin.git $TEMP_DIR

WORKDIR $TEMP_DIR/database
RUN git checkout $BRANCH
RUN pip install -r requirements.txt

WORKDIR $WORK_DIR
RUN rm -rf $TEMP_DIR
HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$APP_HOST:$APP_PORT || exit 1

EXPOSE $APP_PORT
CMD ["sqlite_web", "-H 0.0.0.0", "-p 5001", "/visitor-db/database/visitor_db.db"]
