#!/bin/sh
IPPATTERN="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
THIS="`ifconfig wlan0 | grep  -o -E "$IPPATTERN  B" | grep -o -E "$IPPATTERN"`"
tcpdump -s 0 -i mon0 -e not host $THIS | grep -E -o ' (BSSID|DA|SA).[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f] '  | nc -u 239.255.42.99 5555
