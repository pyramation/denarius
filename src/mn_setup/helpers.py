# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess
import os.path
import json
import codecs
import os
import sys
import warnings
import re
from collections import OrderedDict

if 'MN_ALIAS' in os.environ:
    ALIAS=os.environ['MN_ALIAS']
else:
    ALIAS='denarius'

if 'MN_PORT' in os.environ:
    PORT=os.environ['MN_PORT']
else:
    PORT=19999

if 'DATADIR' in os.environ:
    DATADIR=os.environ['DATADIR']
else:
    DATADIR='%s/.denarius' % os.environ['HOME']

DAEMON_PATH='./denariusd' # TODO assumes you are running from the src dir, please change
MASTERCONF='%s/masternode.conf' % DATADIR
DCONF='%s/denarius.conf' % DATADIR

__escape_decoder = codecs.getdecoder('unicode_escape')
__posix_variable = re.compile('\$\{[^\}]*\}')

def get_config_path():
    return DCONF

def get_config():
    return OrderedDict(parse_config(get_config_path()))

def ensure_config_exists():
    conf = get_config_path()
    if not os.path.isfile(conf):
      raise Exception("%s is missing" % conf)

def ensure_config_does_not_exist():
    conf = get_config_path()
    if os.path.isfile(conf):
      raise Exception("%s already exists" % conf)

def get_port():
  return PORT

def get_mn_config_path():
    return MASTERCONF

def decode_escaped(escaped):
    return __escape_decoder(escaped)[0]

def parse_config(config_path):
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)

            # Remove any leading and trailing spaces in key, value
            k, v = k.strip(), v.strip().encode('unicode-escape').decode('ascii')

            if len(v) > 0:
                quoted = v[0] == v[-1] in ['"', "'"]

                if quoted:
                    v = decode_escaped(v[1:-1])

            yield k, v

def write_mn_config(opts):
    conf=get_config()
    with open(get_mn_config_path(), "w") as f:
        f.write('%s %s:%s %s %s %s' % (opts['alias'].strip(), conf['externalip'], conf['port'], conf['masternodeprivkey'], opts['txhash'], opts['txindex']))
    return True

def write_config(config):
    with open(get_config_path(), "w") as f:
        for k, v in config.items():
            line='%s=%s' % (k, v)
            f.write('%s\n' % line.strip())
    return True

def get_random_alias():
    return "%s%s" % (ALIAS, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_random_rpcpassword():
    return subprocess.check_output(["openssl", "rand", "-hex", "22"])

def get_random_rpcuser(name):
    return "%s-%s" % (name, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_external_ip():
    return subprocess.check_output(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"]).strip()

def get_masternode_key():
    try:
      return subprocess.check_output([DAEMON_PATH, "masternode","genkey"])
    except subprocess.CalledProcessError as e:
      raise Exception( "cannot generate a masternode key" )

def get_masternode_outputs():
    try:
      return json.loads(subprocess.check_output([DAEMON_PATH, "masternode","outputs"]))
    except subprocess.CalledProcessError as e:
      raise Exception( "cannot generate a masternode outputs" )
