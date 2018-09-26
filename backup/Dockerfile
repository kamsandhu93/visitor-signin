FROM python:2.7-alpine
MAINTAINER NHS Digital

#declare arguments
ARG BRANCH
ARG API_TOKEN
ARG DB_FILE

ARG WORK_DIR=/visitor-back
ARG TEMP_DIR=/visitor-back-temp
ARG DB_PATH=$WORK_DIR/database
ARG LOG_PATH=$WORK_DIR/log
ARG CONFIG_NAME=db_ops.cfg

#install packages
RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

#create work directory structure
RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

RUN git clone https://github.com/kamsandhu93/visitor-signin.git $TEMP_DIR

WORKDIR $TEMP_DIR/backup
RUN git checkout $BRANCH
COPY db_ops.py $WORK_DIR
RUN pip install -r requirements.txt

WORKDIR $WORK_DIR

#create config for service
RUN touch $CONFIG_NAME
RUN echo [DEFAULT] >> $CONFIG_NAME
RUN echo DropboxToken=$API_TOKEN >> $CONFIG_NAME
RUN echo DatabaseFile=$DB_FILE >> $CONFIG_NAME
RUN echo DatabaseDir=$WORK_DIR/database >> $CONFIG_NAME
RUN echo LogDir=$WORK_DIR/log >> $CONFIG_NAME

#cleanup
RUN rm -rf $TEMP_DIR

CMD ["python", "db_ops.py"]
