#!/bin/bash
directories=("/opt/visitor-db/" "/opt/visitor-db/database/" "/opt/visitor-db/log/" "/opt/visitor-db/log/flask" "/opt/visitor-db/log/backup/")

function createDir () {
    if [ ! -d "$1" ]; then
        echo "Created: $1"
        mkdir $1
    fi
}

# ensure running as root
if [ "$(id -u)" != "0" ]; then
  exec sudo "$0" "$@"
fi

#parse command line options
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
        -t|--token)
        TOKEN=$2
        shift
        shift
        ;;
        *)
        shift
        ;;
    esac
done

cmd="docker-compose up"

#build command to run
if [ "$FORCE_BUILD" = true ]; then
    cmd+=" --build"
fi

if [ ! "$DEBUG" = true ]; then
    cmd+=" -d"
fi

if [ -z "$TOKEN" ]; then
    echo "Did not supply dropbox token"
    exit 1
fi

for directory in ${directories[*]}
do
    createDir "$directory"
done

export DROPBOX_TOKEN="$TOKEN"

$cmd
