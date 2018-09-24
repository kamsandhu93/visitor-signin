FROM python:2.7-alpine
MAINTAINER NHS Digital

ENV WORK_DIR /visitor-app
ENV TEMP_DIR /visitor-app-temp
ENV DB_FILE visitor_db.db
ENV DB_PATH ${WORK_DIR}/database/${DB_FILE}
ENV BRANCH tw-docker
ENV APP_PORT 5000

RUN apk update && apk upgrade \
 && apk add git \
 && apk add curl \
 && rm -rf /var/cache/apk/*

RUN mkdir ${WORK_DIR}
RUN git clone https://github.com/kamsandhu93/visitor-signin.git ${TEMP_DIR}
WORKDIR ${TEMP_DIR}/flask_app
RUN git checkout ${BRANCH}
COPY main.py ${WORK_DIR}
RUN mkdir ${WORK_DIR}/visitor_app
COPY visitor_app/ ${WORK_DIR}/visitor_app/
RUN pip install -r requirements.txt
WORKDIR ${WORK_DIR}
RUN rm -rf ${TEMP_DIR}

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://localhost:${APP_PORT} || exit 1

EXPOSE ${APP_PORT}
CMD ["python", "main.py"]
