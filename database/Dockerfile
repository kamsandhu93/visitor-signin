FROM python:2.7-alpine
MAINTAINER NHS Digital

ENV WRKDIR /visitor-db
ENV TMPDIR /visitor-db-temp
ENV WEB_PORT 5001
ENV BRANCH tw-docker

RUN apk update && apk upgrade \
  && apk add git \
  && apk add curl \
  && rm -rf /var/cache/apk/*

RUN mkdir ${WRKDIR}
RUN git clone https://github.com/kamsandhu93/visitor-signin.git ${TMPDIR}
WORKDIR ${TMPDIR}
RUN git checkout ${BRANCH}
RUN pip install -r requirements.txt
WORKDIR ${WRKDIR}
RUN rm -rf ${TMPDIR}

EXPOSE ${WEB_PORT}
CMD ["sqlite_web", "-p", "5001", ${WRKDIR}]
