FROM python:3.7-slim

LABEL maintainer="NHS Digital Delivery Centre,  Team-Grads"

ARG WORK_DIR=/home/printservice

ENV LOG_PATH /home/log/print.log

COPY printing/requirements.txt $WORK_DIR/requirements.txt

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
 libcairo2 \
 libpango-1.0-0 \
 libpangocairo-1.0-0 \
 libgdk-pixbuf2.0-0 \
 shared-mime-info \
 #install python packages
 && pip3 install -qr $WORK_DIR/requirements.txt \
 # purge cache
 && rm -rf /var/lib/apt/lists/* \
 #make working directories
 && mkdir /home/log \
 && touch /etc/cups/client.conf

COPY /printing $WORK_DIR/.
COPY /shared $WORK_DIR/shared

WORKDIR $WORK_DIR

HEALTHCHECK --interval=1m30s --timeout=10s --retries=10 \
    CMD curl --fail http://$HOST:$PORT/status || exit 1

EXPOSE ${PORT}

CMD ["/bin/bash", "start.sh"]
