import socket
import struct
import os
import sets
import multiprocessing
import time
from settings import *
import MySQLdb as mdb
import traceback
import sys
socket.setdefaulttimeout(5)


def init():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock
    
def listen(sock, stop_event, db):    
    datasetDict = {}
    lastdb = time.time()
    c = db.cursor()
    while(not stop_event.is_set()):
      try:
          data,addr = sock.recvfrom(1500)
          dataset = datasetDict.get(addr[0],None)
          if dataset == None:
             dataset = sets.Set([])
             datasetDict[addr[0]]  = dataset

          lines = data.split("\n")
          dataset.update([s[3:].replace("ID:","") for s in [l.strip() for l in lines if l.count(":")==6] if s[:2] in ("DA","SA","TA","RA","BS")])
      except:
            #traceback.print_exc(file=sys.stdout)
            pass
            
      if time.time() - lastdb > DBFREQ:
          timestr = time.strftime(DATETIMESTRFORMAT)
          for source in datasetDict:
              dataset = datasetDict[source]
              for d in dataset:
                   if int(d[1:2],16) & 1 == 0 and len(d)==17:
                       sql = "insert into visit (startDateTime, mac, source) values (%s,%s,%s)"
                       c.execute(sql,(timestr, d, source))
                       #print sql
              db.commit()        
          datasetDict = {}             
          lastdb = time.time()
      
      
def start():
    conn = mdb.connect(SERVER, USER, PASSWORD, DB);

    stopevent = multiprocessing.Event()
    stopevent.clear()
    sock = init()
    t = multiprocessing.Process(target=listen, args=(sock, stopevent, conn))    
    t.start()
    return t,stopevent
    
def stop(listenthread, stopevent):
    stopevent.set()
    listenthread.join()
      
