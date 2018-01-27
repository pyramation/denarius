import subprocess
import json
import os
import os.path
from collections import OrderedDict
from helpers import parse_config
from helpers import write_config
from helpers import write_mn_config
from helpers import get_config_path
from helpers import get_mn_config_path
from helpers import get_random_alias
from helpers import get_external_ip

ALIAS= os.environ['MN_ALIAS']
DCONF=get_config_path()
MNCONF=get_mn_config_path()
PORT=19999
ip=get_external_ip()

if not os.path.isfile(DCONF):
  raise Exception("%s is missing" % DCONF)

try:
  outputs=subprocess.check_output(["./denariusd", "masternode","outputs"])
except subprocess.CalledProcessError as e:
  raise Exception( "cannot generate a masternode outputs" )

print outputs

outjson=json.loads(outputs)
conf=OrderedDict(parse_config(DCONF))
mconf=OrderedDict()
mconf['alias'] = get_random_alias(ALIAS)
mconf['txhash'] = next(iter(outjson))
mconf['txindex'] = outjson.values()[0]
write_mn_config(MNCONF, conf, mconf)
