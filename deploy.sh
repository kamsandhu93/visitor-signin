#!/bin/bash

db_dir="/opt/visitor-db/"
db_file="visitor_db.db"

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

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -b|--build)
        FORCE_BUILD=true
        shift
        ;;
        -d|--debug)
        DEBUG=true
        shift
        ;;
        *)
        shift
        ;;
    esac
done

cmd="docker-compose up"

if [ "$FORCE_BUILD" = true ]; then
    cmd+=" --build"
fi

if [ ! "$DEBUG" = true ]; then
    cmd+=" -d"
fi

$cmd
