tcpdump -s 0 -U -n -w - -i mon0 not host 192.168.55.1 | nc 192.168.55.168 9999
