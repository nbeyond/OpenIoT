#!/usr/bin/env python

# HereOnNbeyond.py is a python code to have this pi's information read and sent to nbeyond,
the ground control server.

# 2016. 06.10 by Chan-Hee Park

import subprocess
import time
from time import gmtime, strftime
import datetime

# Now get the vpn generated ip and let nbeyond know
argdate = 'ifconfig'
pipe=subprocess.Popen(argdate,shell=True,stdout=subprocess.PIPE)
ifconfig = pipe.communicate()
tun = ifconfig[0].split("P-t-P:")
tunBefore = tun[0]
tunProcessed = tunBefore.split(":")
ip_pi = tunProcessed[-1]

print ip_pi
