#!/bin/bash
red='\033[0;31m'
end='\033[0m'
green='\033[0;32m'

while getopts ":t: :h" opt; do
    case ${opt} in
        h )
            echo "Usage:"
            echo "    -h        Display help"
            echo "    -t        Operation type (set or unset)"
            exit 0
            ;;
        t )
            action=$OPTARG
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

if [[ $action != "set" ]] && [[ $action != "unset" ]]; then
    printMsg "${red}Please select an operation type (see 'setup_adhoc.sh -h') ${end}"
    exit 1
fi
