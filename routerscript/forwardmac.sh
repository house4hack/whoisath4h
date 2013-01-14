#!/bin/sh
IPPATTERN="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
MACPATTERN="([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
THIS="`ifconfig wlan0 | grep  -o -E "$IPPATTERN  B" | grep -o -E "$IPPATTERN"`"
THISMAC="`ifconfig wlan0 | grep  -o -E "$MACPATTERN"`" 
tcpdump -s 0 -i mon0 -nne "not host $THIS and (type data or type ctl) and not ether host $THISMAC and ether[0] & 1 = 0" | grep -E -o " (BSSID|DA|SA|TA|RA).$MACPATTERN "  | nc -u 239.255.42.99 5555
