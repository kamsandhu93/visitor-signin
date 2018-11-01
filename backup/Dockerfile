FROM python:3.7-alpine
LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

#declare arguments
ARG API_TOKEN
ARG DB_FILE

ARG WORK_DIR=/backupservice
ARG CONFIG_NAME=$WORK_DIR/database_operations.cfg

COPY requirements.txt /tmp/

#install packages
RUN apk update && apk upgrade \
 && apk add curl \
 #install pip packages
 && pip install -r /tmp/requirements.txt \
 #purge cache
 && rm -rf /var/cache/apk/* \
 && rm /tmp/requirements.txt \
 #create work directory structure
 && mkdir $WORK_DIR \
 && mkdir $WORK_DIR/log \
 && mkdir $WORK_DIR/database \
 #create config for service
 && touch $CONFIG_NAME \
 && echo [DEFAULT] >> $CONFIG_NAME \
 && echo DropboxToken=$API_TOKEN >> $CONFIG_NAME \
 && echo DatabaseFile=$DB_FILE >> $CONFIG_NAME \
 && echo DatabaseDir=$WORK_DIR/database >> $CONFIG_NAME \
 && echo LogDir=$WORK_DIR/log >> $CONFIG_NAME

COPY database_operations.py $WORK_DIR/
COPY database.py $WORK_DIR/

WORKDIR $WORK_DIR

CMD ["python", "database_operations.py", "-s", "-o", "backup"]
