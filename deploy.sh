#!/bin/bash
rootPath="/opt/visitor-db"
directories=("$rootPath" "$rootPath/database" "$rootPath/log" "$rootPath/log/flask" "$rootPath/log/backup")
dbName="visitor_db.db"
dbPath="$rootPath/database/$dbName"
branch="master"

red='\033[0;31m'
end='\033[0m'
green='\033[0;32m'

function createDir () {
    if [ ! -d "$1" ]; then
        {
            mkdir $1
        } || {
            exit 1
        }
        echo -e "${green}Created: $1${end}"
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
        recreate=true
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
        -r|--recreate)
        recreate=true
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
    echo -e "${red}Did not supply dropbox token${end}"
    exit 1
fi

for directory in ${directories[*]}
do
    createDir "$directory"
done

if [ ! -f "$dbPath" ]; then
    {
        echo "Database not found, downloading database..."
        curl -X POST https://content.dropboxapi.com/2/files/download \
        --header "Authorization: Bearer $token" \
        --header "Dropbox-API-Arg: {\"path\": \"/$dbName\"}" \
        --output "$dbPath"
        echo -e "${green}Database downloaded to: $dbPath${end}"
    } || {
        exit 1
    }
fi

export DROPBOX_TOKEN="$token"
export DB_FILE="$dbName"
export BRANCH="$branch"

cmd="docker-compose up"

#build command to run
if [ "$forceBuild" = true ]; then
    docker-compose build --no-cache
fi

if [ "$recreate" = true ]; then
    cmd="docker-compose up --force-recreate"
fi

if [ ! "$debug" = true ]; then
    cmd+=" -d"
fi

$cmd
