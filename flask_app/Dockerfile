FROM python:2.7-alpine
MAINTAINER NHS Digital

ARG BRANCH
ARG DB_FILE

ARG WORK_DIR=/visitor-app
ARG TEMP_DIR=/visitor-app-temp
ENV DB_PATH=$WORK_DIR/database/$DB_FILE
ARG APP_PORT=5000
ARG APP_HOST=0.0.0.0
ARG CONFIG_NAME=$WORK_DIR/main.cfg

RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

RUN mkdir $WORK_DIR
RUN mkdir $WORK_DIR/log
RUN mkdir $WORK_DIR/database

RUN git clone https://github.com/kamsandhu93/visitor-signin.git $TEMP_DIR

WORKDIR $TEMP_DIR/flask_app
RUN git checkout $BRANCH
COPY main.py $WORK_DIR
RUN mkdir $WORK_DIR/visitor_app
COPY visitor_app/ $WORK_DIR/visitor_app/
RUN pip install -r requirements.txt

WORKDIR $WORK_DIR

RUN touch $CONFIG_NAME
RUN echo [DEFAULT] >> $CONFIG_NAME
RUN echo LogDir=$WORK_DIR/log >> $CONFIG_NAME
RUN echo Host=$APP_HOST >> $CONFIG_NAME
RUN echo Port=$APP_PORT >> $CONFIG_NAME

RUN rm -rf $TEMP_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$APP_HOST:$APP_PORT || exit 1

EXPOSE $APP_PORT
CMD ["python", "main.py", "-c", "/visitor-app/main.cfg"]
