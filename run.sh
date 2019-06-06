#!/bin/bash
dbName="visitor_db.db"
hostIp="127.0.0.1"

rootPath="/opt/visitorsignin"
offlineBackupPath="$rootPath/offline_backup"


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

# Start of main script
while getopts ":t: :f: :H: :b: :hdr" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -t        Dropbox API token (Mandatory)"
            echo "    -H        Host IP address"
            echo "    -d        Start in debug mode"
            echo "    -r        Force recreate containers"
            echo "    -f        File name of sqlite database (default: visitor_db.db)"
            echo "    -b        Offline backup path (default: /opt/visitorsignin/offline_backup)"
            exit 0
            ;;
        t )
            token=$OPTARG
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
        H )
            hostIp=$OPTARG
            ;;
        b )
            offlineBackup=$OPTARG
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

rootDirectories=("$rootPath" "$rootPath/database" "$rootPath/log" "$offlineBackupPath" "$rootPath/template")

createDirectories ${rootDirectories[*]}

sudo cp -r ./printing/template/. "$rootPath/template/."

export DROPBOX_TOKEN=$token
export DB_FILE=$dbName
export REQUEST_HOST=$hostIp
export OFFLINE_BACKUP_PATH=$offlineBackupPath

cmd="sudo -E docker-compose up"

if [[ $recreate = true ]]; then
    cmd+=" --force-recreate"
fi

if [[ ! $debug = true ]]; then
    cmd+=" -d"
fi

$cmd
