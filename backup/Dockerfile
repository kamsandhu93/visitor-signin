FROM python:2.7-alpine
MAINTAINER NHS Digital

ARG WORK_DIR=/visitor-back
ARG TEMP_DIR=/visitor-back-temp
ARG DB_FILE=visitor_db.db
ARG DB_PATH=$WORK_DIR/database/$DB_FILE
ARG LOG_PATH=$WORK_DIR/log
ARG BRANCH
ARG API_TOKEN

RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

RUN git clone https://github.com/kamsandhu93/visitor-signin.git $TEMP_DIR

WORKDIR $TEMP_DIR/backup
RUN git checkout $BRANCH
COPY backup.py $WORK_DIR
RUN pip install -r requirements.txt
RUN chmod u+x $WORK_DIR/backup.py
RUN echo "* * * * *" $WORK_DIR/backup.py -t $API_TOKEN -p $DB_PATH -l $LOG_PATH > /etc/crontabs/root

WORKDIR $WORK_DIR
RUN rm -rf $TEMP_DIR

CMD ["crond", "-f"]
