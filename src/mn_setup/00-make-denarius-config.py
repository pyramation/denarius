from collections import OrderedDict
from helpers import write_config, ensure_config_does_not_exist, get_random_rpcuser, get_random_rpcpassword, use_testnet

ensure_config_does_not_exist()

conf=OrderedDict()

conf['rpcuser'] = get_random_rpcuser("denariusrpc")
conf['rpcpassword'] = get_random_rpcpassword()
conf['testnet'] = use_testnet()
conf['daemon'] = 1
conf['staking'] = 0

write_config(conf)
