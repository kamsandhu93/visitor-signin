#!/bin/bash
directories=("/opt/visitor-db/" "/opt/visitor-db/database/" "/opt/visitor-db/log/" "/opt/visitor-db/log/flask" "/opt/visitor-db/log/backup/")
dbName="visitor_db.db"
branch="master"

function createDir () {
    if [ ! -d "$1" ]; then
        mkdir $1
        echo "Created: $1"
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
        forceBuild=true
        shift
        ;;
        -d|--debug)
        debug=true
        shift
        ;;
        -t|--token)
        token=$2
        shift
        shift
        ;;
        -db|--database)
        dbName=$2
        shift
        shift
        ;;
        -br|--branch)
        branch=$2
        shift
        shift
        ;;
        *)
        shift
        ;;
    esac
done

if [ -z "$token" ]; then
    echo "Did not supply dropbox token"
    exit 1
fi

export DROPBOX_TOKEN="$token"
export DB_FILE="$dbName"
export BRANCH="$branch"

cmd="docker-compose up"

#build command to run
if [ "$forceBuild" = true ]; then
    docker-compose build --no-cache
    cmd="docker-compose up --force-recreate"
fi

if [ ! "$debug" = true ]; then
    cmd+=" -d"
fi



for directory in ${directories[*]}
do
    createDir "$directory"
done

$cmd
