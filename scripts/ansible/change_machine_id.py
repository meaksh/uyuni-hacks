#!/usr/bin/python3
import argparse 
import yaml
import json
import os
import random
import hashlib
import subprocess
import xmlrpc.client as xmlrpclib


SATELLITE_URL = "http://suma41-srv.tf.local/rpc/api"
SATELLITE_LOGIN = "admin"
SATELLITE_PASSWORD = "admin"
LOCAL_ANSIBLE_CACHE = "/var/cache/ansible/"

parser = argparse.ArgumentParser(description='Bootstrap an Ansible systems as minion in SUSE Manager using salt-ssh.')
parser.add_argument("-s", "--systemid", required=True, dest="systemid", help="the system id for the server in SUSE Manager")
parser.add_argument("-m", "--machineid", required=True, dest="machineid", help="the machine id to set")
args = parser.parse_args()


# Connect to SUSE Manager XMLRPC API and import missing Ansible systems
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

print("* Set machine ID from the Ansible system {} to: {}".format(args.systemid, args.machineid))
client.system.changeMachineIdForSystem(key, int(args.systemid), args.machineid)

# Logging out
client.auth.logout(key)

# Done
print("* Done!")
