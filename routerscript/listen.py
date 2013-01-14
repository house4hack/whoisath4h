import socket
import struct
import os

MCAST_GRP = '239.255.42.99'
MCAST_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

import sets
dataset = sets.Set([])
while True:
  data,addr = sock.recvfrom(1500)
  #print addr
  lines = data.split("\n")
  dataset.update([("ID"+s[2:]).replace("IDSID","BS") for s in [l.strip() for l in lines if l.count(":")==6] if s[:2] in ("DA","SA","TA","RA") or s.startswith("BSSID")])
  maclist = []
  maclist.extend(["%s from %s" % (d,addr[0]) for d in dataset if len(d)==20 and int(d[4:5],16) & 1 == 0])
  maclist.sort()
  os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
  print "\n".join(maclist)
