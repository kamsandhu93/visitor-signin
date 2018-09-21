#!/bin/bash

db_dir=/opt/visitor-db/
db_file=visitor_db.db

# ensure running as root
if [ "$(id -u)" != "0" ]; then
  exec sudo "$0" "$@"
fi

if [ ! -d $db_dir ]; then
    mkdir $db_dir
fi

if [ ! -f $db_file ]; then
    cp $db_file $db_dir
fi

docker-compose up --build
