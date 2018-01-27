# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess
import os.path
import codecs
import os
import sys
import warnings
import re
from collections import OrderedDict

__escape_decoder = codecs.getdecoder('unicode_escape')
__posix_variable = re.compile('\$\{[^\}]*\}')

def get_config_path():
    return "%s/.denarius/denarius.conf" % os.environ['HOME']

def get_mn_config_path():
    return "%s/.denarius/masternode.conf" % os.environ['HOME']

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

def write_mn_config(conf_path, conf, opts):
    with open(conf_path, "w") as f:
        f.write('%s %s:%s %s %s %s' % (opts['alias'].strip(), conf['externalip'], conf['port'], conf['masternodeprivkey'], opts['txhash'], opts['txindex']))
    return True

def write_config(conf_path, conf_as_dict):
    with open(conf_path, "w") as f:
        for k, v in conf_as_dict.items():
            line='%s=%s' % (k, v)
            f.write('%s\n' % line.strip())
    return True

def get_random_alias(name):
    return "%s%s" % (name, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_random_rpcpassword():
     return subprocess.check_output(["openssl", "rand", "-hex", "22"])

def get_random_rpcuser(name):
    return "%s-%s" % (name, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_external_ip():
   return subprocess.check_output(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"]).strip()
