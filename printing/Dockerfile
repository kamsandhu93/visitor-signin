FROM python:3.7-slim

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG WORK_DIR=/printservice

ENV LOG_PATH $WORK_DIR/log/print.log

COPY /requirements.txt $WORK_DIR/requirements.txt

RUN apt-get -qq update \
 && apt-get -qq install -y \
 bash \
 curl \
 cups \
 cups-client \
 python3-dev \
 libcups2-dev \
 iproute2 \
 fonts-liberation \
 libffi-dev \
 #install python packages
 && pip3 install -qr $WORK_DIR/requirements.txt \
 #remove build dependencies and purge cache
 && apt-get -qq purge -y --auto-remove \
 gcc \
 libcups2-dev \
 python3-dev \
 libffi-dev \
 && rm -rf /var/lib/apt/lists/* \
 #make working directories
 && mkdir $WORK_DIR/log \
 && touch /etc/cups/client.conf

COPY . $WORK_DIR/.

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE ${PORT}

CMD ["/bin/bash", "start.sh"]