#!/bin/bash
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

function checkOrig () {
    for file in $@
    do
        if [[ ! -f $file ]]; then
            printMsg "${red}Original $file was not found, restore cancelled${end}"
            exit 1
        fi
    done
}

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

echo -e "${red}ONLY USE THIS SCRIPT ON A RASPBERRY PI${end}"
echo "Continue (y/N): "

read startScript

if [[ ! $startScript =~ ^[Yy]$ ]]; then
    echo -e "${red}Cancelled${end}"
    exit 0
fi

interfaces=/etc/network/interfaces
interfacesOrig="${interfaces}.orig"

hostapd=/etc/init.d/hostapd
hostapdOrig="${hostapd}.orig"

hostapdConf=/etc/hostapd/hostapd.conf

dnsmasqConf=/etc/dnsmasq.conf
dnsmasqConfOrig="${dnsmasqConf}.orig"

dhcpcdConf=/etc/dhcpcd.conf
dhcpcdConfOrig="${dhcpcdConf}.orig"

origFiles=("$interfacesOrig" "$hostapdOrig" "$dnsmasqConfOrig" "$dhcpcdConfOrig")

if [[ $action = "set" ]]; then
    sudo mv $interfaces $interfacesOrig
    sudo cp interfaces $interfaces

    sudo mv $hostapd $hostapdOrig
    sudo cp hostapd $hostapd

    sudo mv $dnsmasqConf $dnsmasqConfOrig
    sudo cp dnsmasq.conf $dnsmasqConf

    sudo mv $dhcpcdConf $dhcpcdConfOrig
    sudo cp dhcpcd.conf $dhcpcdConf

    sudo cp hostapd.conf $hostapdConf
elif [[ $action = "unset" ]]; then
    checkOrig ${origFiles[*]}

    sudo rm $interfaces
    sudo mv $interfacesOrig $interfaces

    sudo rm $hostapd
    sudo mv $hostapdOrig $hostapd

    sudo rm $hostapdConf

    sudo rm $dnsmasqConf
    sudo mv $dnsmasqConfOrig $dnsmasqConf

    sudo rm $dhcpcdConf
    sudo mv $dhcpcdConfOrig $dhcpcdConf
else
    printMsg "${red}Please select an operation type (see 'setup_adhoc.sh -h') ${end}"
    exit 1
fi
