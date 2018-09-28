FROM python:2.7-alpine
MAINTAINER NHS Digital

#declare arguments
ARG API_TOKEN
ARG DB_FILE

ARG WORK_DIR=/visitor-back
ARG CONFIG_NAME=$WORK_DIR/db_ops.cfg

#install packages
RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

#create work directory structure
RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

ADD db_ops.py $WORK_DIR
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR $WORK_DIR

#create config for service
RUN touch $CONFIG_NAME
RUN echo [DEFAULT] >> $CONFIG_NAME
RUN echo DropboxToken=$API_TOKEN >> $CONFIG_NAME
RUN echo DatabaseFile=$DB_FILE >> $CONFIG_NAME
RUN echo DatabaseDir=$WORK_DIR/database >> $CONFIG_NAME
RUN echo LogDir=$WORK_DIR/log >> $CONFIG_NAME

CMD ["python", "db_ops.py", "-s", "-o", "backup"]
