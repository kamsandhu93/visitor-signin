#!/bin/bash
while getopts ":s: :h" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -s        Name of container to build for building single container"
            exit 0
            ;;
        s )
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

if [[ -z $container ]]; then
    sudo docker-compose build
else
    sudo docker-compose build $container
fi
