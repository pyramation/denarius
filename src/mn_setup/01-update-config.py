import subprocess
import json
import os
import os.path
from collections import OrderedDict
from helpers import parse_config
from helpers import write_config
from helpers import get_config_path
from helpers import get_external_ip

DCONF=get_config_path()
PORT=19999

if not os.path.isfile(DCONF):
  raise Exception("%s is missing" % DCONF)

conf=OrderedDict(parse_config(DCONF))

ip=get_external_ip()

try:
  masternodeprivkey=subprocess.check_output(["./denariusd", "masternode","genkey"])
except subprocess.CalledProcessError as e:
  raise Exception( "cannot generate a masternode key" )

conf['listen'] = 1
conf['logtimestamps'] = 1
conf['maxconnections'] = 256
conf['port'] = PORT
conf['masternode'] = 1
conf['externalip'] = ip
conf['bind'] = ip
conf['masternodeaddr'] = "%s:%s" % (ip, PORT)
conf['masternodeprivkey'] = masternodeprivkey

write_config(DCONF, conf)
