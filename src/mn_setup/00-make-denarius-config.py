import os.path
from collections import OrderedDict
from helpers import write_config
from helpers import get_config_path
from helpers import get_random_rpcpassword
from helpers import get_random_rpcuser

DCONF=get_config_path()

if os.path.isfile(DCONF):
  raise Exception("%s exists" % DCONF)

conf=OrderedDict()

conf['rpcuser'] = get_random_rpcuser("denariusrpc")
conf['rpcpassword'] = get_random_rpcpassword()
conf['testnet'] = 1
conf['daemon'] = 1
conf['staking'] = 0

write_config(DCONF, conf)
