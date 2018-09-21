FROM python:2.7-alpine
MAINTAINER NHS Digital

ENV WRKDIR /visitor-db
ENV TMPDIR /visitor-db-temp
ENV WEB_PORT 5001
ENV BRANCH master

RUN apk update && apk upgrade \
  && apk add git \
  && apk add curl \
  && rm -rf /var/cache/apk/*

RUN mkdir ${WRKDIR}
RUN git clone https://github.com/kamsandhu93/visitor-signin.git ${TMPDIR}
WORKDIR ${TMPDIR}/database
RUN git checkout ${BRANCH}
RUN pip install -r requirements.txt
WORKDIR ${WRKDIR}
RUN rm -rf ${TMPDIR}

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://localhost:${WEB_PORT} || exit 1

EXPOSE ${WEB_PORT}
CMD ["sqlite_web", "-H 0.0.0.0", "-p 5001", "/visitor-db/visitor_db.db"]
