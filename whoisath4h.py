import cherrypy
from cherrypy import request
from settings import *
import whoisath4hlib.db as db
import whoisath4hlib.listen as listen
from whoisath4hlib.saplugin import SAEnginePlugin, SATool
from sqlalchemy import and_, or_
from scapy.all import srp,Ether,ARP,conf
import time
import traceback, sys
import threading
import hashlib

# Jinja templating engine
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))


def md5str(str):
   m = hashlib.md5()
   m.update(str + SALT)
   return m.hexdigest()
   
def safemin(seq):
   if(len(seq) ==0):
       return 0
   else:
       return min(seq)  
       
class visit():
   def __init__(self, name, resolved, obscure=True):
       self.name = name
       self.md5 = md5str(name)
       self.resolved = resolved
       if resolved or not obscure:
            self.title = name
       else:     
            self.title = "Unknown ("+name[8:]+")"                
                 

class WhoIsAtH4H(object):       
    lastArpingTime = 0
    listenthread,stop_event = listen.start()
    
    def __init__(self):
        cherrypy.engine.subscribe('stop', self.stop)
        
     
    def getAsTime(self, startdate="", enddate=""):
        try:
            enddate = time.strftime(time.strptime(enddate,DATETIMESTRFORMAT),DATETIMESTRFORMAT)
        except:
            enddate = time.strftime(DATETIMESTRFORMAT)
        try:
            startdate = time.strftime(time.strptime(startdate,DATETIMESTRFORMAT) ,DATETIMESTRFORMAT)
        except:
            startdate = time.strftime(DATETIMESTRFORMAT,time.localtime(time.time() - 5*60))   
        return startdate, enddate    
        
    def isLocal(self):
        ip = request.remote.ip
        return (ip.startswith(IPSTARTWITH) and ip != HOSTIP) or ip==LOCALHOST    
        
    @cherrypy.expose 
    def index(self, startdate="", enddate="", all="0"):

        if self.isLocal():
            obscure = False
        else:
            obscure = True    
  
        if all== "1":
            where = " 1=1 "      
        else:
            where = " (type=0 or type is null) "    

        startdate, enddate = self.getAsTime(startdate,enddate)    
        visits = self.getVisits(startdate,enddate, where)
        visitlist = self.makeVisitList(visits, obscure)

        return env.get_template('index.html').render({'visits':visitlist,'total':len(visitlist),'homeclass':'active', 'local':(not obscure), 'all':all}) 
        
    @cherrypy.expose
    def register(self,lookup=""):
        if not self.isLocal():
            raise cherrypy.HTTPRedirect("index")                
    
        if lookup == "":
            ip = request.remote.ip
            if lookup == "":
                arpans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),timeout=5)
                if len(arpans) == 1:    
                    snd,rcv = arpans[0]
                    lookup = str(rcv.sprintf(r"%Ether.src%"))
                else:
                    lookup =""
        name = ""
        title = ""
        checked = "" 
        otherdevices = []   
        devices = []

        if lookup != "":
            devices = request.db.query(db.Device).filter(or_(db.Device.mac==lookup, db.Device.name==lookup)).all()
        if len(devices)!=0:
            name = devices[0].name
            title = devices[0].title
            mac = devices[0].mac
            if devices[0].type == NORMALUSER:
               checked = ""
            else:
               checked = "checked" 
            otherdevices = [d for d in devices[1:]]      
        else:
            mac = lookup     
            
        return env.get_template('register.html').render({'mac':mac,'name':name,'title':title, 'checked':checked,'registerclass':'active','otherdevices':otherdevices}) 

    @cherrypy.expose
    def submitRegistration(self, mac, title, name, hidden=""):
        if name.strip() != "" and mac.strip() != "":
            devices = request.db.query(db.Device).filter_by(mac=mac.strip()).all()
            if len(devices) == 1:
               device = devices[0]
               device.title = title.strip()
               device.name = name.strip()
               if hidden != "":
                   device.type = HIDDEN
               else:
                   device.type = NORMALUSER     
               request.db.merge(device)    
            elif len(devices)>1:
               for dev in devices[1:]:
                  request.db.delete(dev)   
            else:
               device = db.Device(name.strip(), title.strip(), mac.strip()) 
               if hidden != "":
                   device.type = HIDDEN
               else:
                   device.type = NORMALUSER     
               
               request.db.merge(device)    
        
        raise cherrypy.HTTPRedirect("/")    
        
        
    def makeVisitList(self, visitlist, obscure):
        resolved = [visit(v['name'],1,obscure) for v in visitlist if v['resolved']==1]    
        unresolved = [visit(v['name'],0,obscure) for v in visitlist if v['resolved']==0]
        resolved.extend(unresolved)
        return resolved
        
    """def doArpPing(self):
        WhoIsAtH4H.arpans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ARPIP),timeout=5) 
        print WhoIsAtH4H.arpans  
        return self.arpans      """
            
    def getAddr(self,id):
        md5dict = dict([(md5str(m),m) for m in cherrypy.session.get('maclist',[])])
        print md5dict
        addr = md5dict.get(id,None)
        if(addr == None):
            raise cherrypy.HTTPRedirect("index")
        return addr    


    def getVisits(self,startdate,enddate, where="1=1"):
        visits = []
        try:
            conn = request.db
            try:
                sql = ''' select distinct 
                          case when d.name is null then v.mac else d.name end name,
                          case when d.name is null then 0 else 1 end resolved
                          from visit v 
                          left join device d on v.mac = d.mac     
                          where startDateTime between '%(startdate)s' and '%(enddate)s' 
                          and %(where)s
                          order by name''' % {'startdate':startdate,'enddate':enddate, 'where':where}
                print sql         
                visits = conn.execute(sql).fetchall()

            finally:
                conn.close()
        except:
            traceback.print_exc(file=sys.stdout)
            maxdate = -1 
        return visits      
    
    def getPacketsForAddr(self,startdate, enddate, addr):
        where = " (mac = '%s') " % (addr)
        return self.getPackets(startdate, enddate, where)
        
    def stop(self):
        listen.stop(WhoIsAtH4H.listenthread,WhoIsAtH4H.stop_event)

if __name__=="__main__":
    cherrypy.config.update(whoisath4hconf)
    SAEnginePlugin(cherrypy.engine,WHOISATH4H_DB).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.tree.mount(WhoIsAtH4H(), '/', config=whoisath4hconf)

    cherrypy.engine.start()
    cherrypy.engine.block()
    
