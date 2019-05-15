#!/bin/bash

function loadNvm() {
    if [[ -d ~/.nvm ]]; then
        echo "Node install from NVM found. Using NVM installed node"
        export NVM_DIR=~/.nvm
        source ~/.nvm/nvm.sh
    fi
}

function buildFrontend() {
    loadNvm
    pushd ./frontend
    npm install
    npm run build
    popd
}

while getopts ":s: :hn" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -s        Name of container to build for building single container"
            echo "    -n        Build without using cache"
            exit 0
            ;;
        s )
            container=$OPTARG
            ;;
        n )
            noCache=true
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

command="sudo docker-compose build"

if [[ -z $noCache ]]; then
    command+=" --no-cache"
fi

if [[ -z $container ]]; then
    buildFrontend
    $command
else
    if [[ $container = "frontend" ]]; then
        buildFrontend
    fi
    $command $container
fi
