import os
#WHOISATH4H_BASE_URL = "http://localhost:8080"

whoisath4hconf = os.path.join(os.path.dirname(__file__), 'whoisath4h.conf')
current_dir = os.path.dirname(os.path.abspath(__file__))

WHOISATH4H_DB = "mysql://whoisath4h:whoisath4hp4s5@localhost/whoisath4h"

# ARP
SALT = "h1h2h3h4h"
ARPINGFREQ = 120
ARPIP = "192.168.1.1/24"
LOCALHOST = "disable127.0.0.1"
HOSTIP = "192.168.1.6"

# enum for visitor type
NORMALUSER = 0
HIDDEN = 1
INFRASTRUCTURE = 2

# listen settings
MCAST_GRP = '239.255.42.99'
MCAST_PORT = 5555
DBFREQ = 10

DATETIMESTRFORMAT = '%Y-%m-%d %H:%M:%S'

# listen db connection
DB = 'whoisath4h'
USER = 'whoisath4h'
PASSWORD='whoisath4hp4s5'
SERVER = 'localhost'

#registration
IPSTARTWITH = '192.168.1'


