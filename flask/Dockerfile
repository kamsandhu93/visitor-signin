FROM python:2.7-alpine
MAINTAINER NHS Digital


ENV WRKDIR /visitor-app
ENV TMPDIR /visitor-app-temp
ENV FLASK_PORT 5000


RUN apk update && apk upgrade \
  && apk add git \
  && apk add curl \
  && rm -rf /var/cache/apk/*

RUN mkdir ${WRKDIR}
RUN git clone https://github.com/kamsandhu93/visitor-signin.git ${TMPDIR}
WORKDIR ${TMPDIR}
COPY main.py ${WRKDIR}
COPY requirements.txt ${WRKDIR}
WORKDIR ${WRKDIR}
RUN rm -rf ${TMPDIR}
RUN pip install -r requirements.txt

EXPOSE ${FLASK_PORT}
CMD ["python", "main.py"]
