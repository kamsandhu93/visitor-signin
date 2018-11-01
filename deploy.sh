#!/bin/bash
dbName="visitor_db.db"

red='\033[0;31m'
end='\033[0m'
green='\033[0;32m'

function printMsg () {
    printf "\n"
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
    echo -e $1
    printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
    printf "\n"
}

function checkSuccess () {
    if [[ $? = 0 ]]; then
        printMsg "${green}$1 SUCCESS${end}"
    else
        printMsg "${red}$1 FAILED${end}"
        exit $?
    fi
}

function createDirectories () {
    for directory in $@
    do
        if [[ ! -d $directory ]]; then
            sudo mkdir $directory
            checkSuccess "Create $directory"
        fi
    done
}

function downloadDatabase () {
    if [[ ! -f $dbPath ]]; then
        printMsg "Database not found, downloading database..."
        sudo curl -X POST https://content.dropboxapi.com/2/files/download \
        --header "Authorization: Bearer $token" \
        --header "Dropbox-API-Arg: {\"path\": \"/$dbName\"}" \
        --output "$dbPath"
        checkSuccess "Database download"
    fi
}


# Start of main script
while getopts ":t: :c: :f: :hbdr" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -t        Dropbox API token (Mandatory)"
            echo "    -b        Force rebuild"
            echo "    -d        Start in debug mode"
            echo "    -r        Force recreate containers"
            echo "    -f        File name of sqlite database"
            exit 0
            ;;
        t )
            token=$OPTARG
            ;;
        b )
            rebuild=true
            recreate=true
            ;;
        d )
            debug=true
            ;;
        r )
            recreate=true
            ;;
        f )
            dbName=$OPTARG
            ;;
        c )
            container=$OPTARG
            ;;
        \? )
            echo -e "${red}Invalid option: $OPTARG${end}" 1>&2
            exit 1
            ;;
        : )
            echo -e "${red}Invalid option: $OPTARG requires an argument${end}" 1>&2
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

if [[ -z $token ]]; then
    printMsg "${red}Did not supply dropbox token${end}"
    exit 1
fi

rootPath="/opt/visitorsignin"
rootDirectories=("$rootPath" "$rootPath/database" "$rootPath/log")
dbPath="$rootPath/database/$dbName"

createDirectories ${rootDirectories[*]}

downloadDatabase

export DROPBOX_TOKEN=$token
export DB_FILE=$dbName
export REQUEST_HOST=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep 192.)

cmd="sudo -E docker-compose up"

#build command to run
if [[ $rebuild = true ]]; then
    printMsg "Rebuilding containers"
    sudo -E docker-compose build --no-cache
    checkSuccess "Container build"
elif [[ ! -z $container ]]; then
    printMsg "Rebuilding $container"
    sudo -E docker-compose build --no-cache $container
    checkSuccess "$container build"
    cmd="sudo -E docker-compose up $container"
fi

if [[ $recreate = true ]]; then
    cmd="sudo -E docker-compose up --force-recreate"
fi

if [[ ! $debug = true ]]; then
    cmd+=" -d"
fi

$cmd
