FROM python:3.7-alpine

MAINTAINER NHS Digital Delivery Centre,  Team-Grads

RUN apk update && apk upgrade \
 && apk add wkhtmltopdf \
 && apk add curl \
 && apk add wkhtmltopdf --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted \
 && rm -rf /var/cache/apk/*

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# SHOULD NOT BE HARDCODED HERE
ARG DB_FILE

ENV DB_PATH /app/visitor_app/database/$DB_FILE
ENV PORT 5000
ENV HOST 0.0.0.0
ENV LOG_PATH /app/visitor_app/log/visitor_app.log

ADD ./visitor_app /app/visitor_app
ADD ./generate_pdf /app/generate_pdf
ADD ./main.py /app/
RUN mkdir app/visitor_app/log
RUN mkdir app/visitor_app/database

WORKDIR /app

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE $PORT
CMD ["python3", "main.py"]
