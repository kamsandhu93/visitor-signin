#!/bin/bash

export DATABASE="$DB_PATH/$DB_FILE"
export REQUEST_HOST=$(/sbin/ip route|awk '/default/ { print $3 }')

python3 main.py
