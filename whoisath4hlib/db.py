from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from settings import *

engine = create_engine(WHOISATH4H_DB, echo=True)
Base = declarative_base()
 
########################################################################
class Device(Base):
    """"""
    __tablename__ = "device"
 
    id = Column(Integer, primary_key=True)
    mac = Column(VARCHAR(50))
    title = Column(VARCHAR(50))
    type = Column(Integer)
    name = Column(VARCHAR(50))
 
    #----------------------------------------------------------------------
    def __init__(self, name, title, mac):
        """"""
        self.title = title
        self.mac = mac
        self.type = NORMALUSER
        self.name = name
 
########################################################################
class Visit(Base):
    """"""
    __tablename__ = "visit"
 
    id = Column(Integer, primary_key=True)
    startDateTime = Column(VARCHAR(50))  
    mac = Column(VARCHAR(50))  
    source = Column(VARCHAR(50))  
    
 
    #----------------------------------------------------------------------
    def __init__(self, startDateTime, mac, times):
        """"""
        self.startDateTime = startDateTime    
        self.mac = mac
        self.times = times
 
 
# create tables
Base.metadata.create_all(engine)
