#!/bin/bash

function checkInput () {
    if [ -z "$1" ]; then
        echo "$2"
        exit 1
    fi
}

#parse command line options
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -h|--host)
        HOST="$2"
        shift
        shift
        ;;
        -p|--port)
        PORT="$2"
        shift
        shift
        ;;
        -d|--database)
        DB_FILE="$2"
        shift
        shift
        ;;
        *)
        shift
        ;;
    esac
done

checkInput "$HOST" "Host not found"
checkInput "$PORT" "Port not found"
checkInput "$DB_FILE" "Database file not found"

crond -b &&
sqlite_web -H "$HOST" -p "$PORT" "$DB_FILE"
