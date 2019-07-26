#!/bin/bash
dbName="visitor_db.db"
hostIp="127.0.0.1"

# Start of main script
while getopts ":t: :f: :H: :b: :hdr" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -H        Host IP address"
            echo "    -d        Start in debug mode"
            echo "    -r        Force recreate containers"
            echo "    -f        File name of sqlite database (default: visitor_db.db)"
            echo "    -b        Offline backup path (default: /opt/visitorsignin/offline_backup)"
            exit 0
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
