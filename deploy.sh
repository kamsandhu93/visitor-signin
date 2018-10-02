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

while getopts ":t: :f: :hbdr" opt; do
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

rootPath="/opt/visitor-db"
directories=("$rootPath" "$rootPath/database" "$rootPath/log" "$rootPath/log/flask" "$rootPath/log/backup")
dbPath="$rootPath/database/$dbName"


#create host directories if not exist
for directory in ${directories[*]}
do
    if [[ ! -d $directory ]]; then
        sudo mkdir $directory
        if [[ $? = 0 ]]; then
            printMsg "${green}Created: $directory${end}"
        else
            printMsg "${red}Failed to create: $directory${end}"
            exit $?
        fi
    fi
done


#download db file if not exist
if [[ ! -f $dbPath ]]; then
    printMsg "Database not found, downloading database..."
    sudo curl -X POST https://content.dropboxapi.com/2/files/download \
    --header "Authorization: Bearer $token" \
    --header "Dropbox-API-Arg: {\"path\": \"/$dbName\"}" \
    --output "$dbPath"
    if [[ $? = 0 ]]; then
        echo    "---------------------------------------------"
        echo -e "${green}Database downloaded to: $dbPath${end}"
        echo    "---------------------------------------------"
    else
        echo    "------------------------------------"
        echo -e "${red}Database download failed${end}"
        echo    "------------------------------------"
        exit $?
    fi
fi

#build frontend
printMsg "Building frontend..."
pushd frontend
printMsg "Installing node modules..."
npm install
if [[ $? = 0 ]]; then
    printMsg "${green}npm install success${end}"
else
    printMsg "${red}npm install fail${end}"
    exit $?
fi
npm run build
if [[ $? = 0 ]]; then
    printMsg "${green}Frontend build success${end}"
else
    printMsg "${red}Frontend build fail${end}"
    exit $?
fi
popd

export DROPBOX_TOKEN=$token
export DB_FILE=$dbName

cmd="sudo -E docker-compose up"

#build command to run
if [[ $rebuild = true ]]; then
    printMsg "Rebuilding containers"
    sudo -E docker-compose build --no-cache
    if [[ $? = 0 ]]; then
        printMsg "${green}Container build success${end}"
    else
        printMsg "${red}Container build fail${end}"
        exit $?
    fi
fi

if [[ $recreate = true ]]; then
    cmd="sudo -E docker-compose up --force-recreate"
fi

if [[ ! $debug = true ]]; then
    cmd+=" -d"
fi

$cmd
