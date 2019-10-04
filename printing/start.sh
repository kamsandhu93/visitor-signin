doc#!/bin/bash

#Adds host ip address to cups client conf to allow network printing
clientConf=/etc/cups/client.conf

grep "$( echo -n 'ServerName ';  /sbin/ip route|awk '/default/ { print $3 }'; )" $clientConf
if [[ $? = 1 ]]; then
    rm $clientConf
    { echo -n 'ServerName ';  /sbin/ip route|awk '/default/ { print $3 }'; } >> $clientConf
fi

#start printing api service
python3 main.py
