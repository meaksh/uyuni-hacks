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

SALT_SSH_COMMAND = "salt-ssh --output=json -l info --priv={ssh_identity_file} {host} ansible.targets export=True yaml=True"
SALT_SSH_GET_KEY_COMMAND = "salt-ssh --output=json -l info --priv={ssh_identity_file} {host} file.read {file}"

parser = argparse.ArgumentParser(description='Import Ansible systems in SUSE Manager using salt-ssh.')
parser.add_argument("-H", "--hostname", required=True, dest="hostname", help="hostname for the Ansible controller to get the system inventory from")
parser.add_argument("-i", "--ssh-identity-file", required=True, dest="ssh_identity_file", help="SSH private key")
args = parser.parse_args()

# Get the Ansible inventory via salt-ssh
inventory = None
if not os.path.isdir(LOCAL_ANSIBLE_CACHE):
    os.mkdir(LOCAL_ANSIBLE_CACHE)
_cmd = SALT_SSH_COMMAND.format(**{"ssh_identity_file": args.ssh_identity_file, "host": args.hostname})
print("* Importing Ansible inventory via: {}".format(_cmd))
salt_ssh_proc = subprocess.Popen(_cmd, shell=True,  stdout=subprocess.PIPE)
output = salt_ssh_proc.communicate()
try:
    inventory = yaml.load(json.loads(output[0])[args.hostname], Loader=yaml.SafeLoader)
except Exception as exc:
    print("-- Error getting JSON and/or YAML response from salt-ssh: {}".format(exc))
    exit(1)

# Check for SSH keys that are referenced on the Ansible inventory
ansible_ssh_keys = []
ansible_hosts = []

def _process_node(node):
    for i in node.keys():
        if isinstance(node[i], dict):
            if not node[i].keys():
                # Is final host node.
                if i not in ansible_hosts:
                    ansible_hosts.append(i)
            else:
                _process_node(node[i])
        elif i == 'ansible_ssh_private_key_file':
            if node[i] not in ansible_ssh_keys:
                ansible_ssh_keys.append(node[i])

_process_node(inventory)

if ansible_ssh_keys:
    print("* Detected SSH keys on the Ansible Inventory:")
    for key in ansible_ssh_keys:
        print("- SSH key: {}".format(key))
        
# Download detected SSH keys
downloaded_ssh_keys = {}
if ansible_ssh_keys:
    print("* Downloading the SSH keys from the Ansible Inventory via salt-ssh:")
    for key in ansible_ssh_keys:
        _cmd = SALT_SSH_GET_KEY_COMMAND.format(**{"ssh_identity_file": args.ssh_identity_file, "host": args.hostname, "file": key})
        salt_ssh_proc = subprocess.Popen(_cmd, shell=True,  stdout=subprocess.PIPE)
        output = salt_ssh_proc.communicate()
        try:
            downloaded_ssh_keys[key] = json.loads(output[0])[args.hostname]
            key_file_path = os.path.join(LOCAL_ANSIBLE_CACHE, "ansible-ssh-key-{}.key".format(hashlib.md5(downloaded_ssh_keys[key].encode()).hexdigest()))
            if os.path.isfile(key_file_path):
                print("- Already cached SSH key at: {}".format(key_file_path))
                downloaded_ssh_keys[key] = key_file_path
                break
            fp = os.open(key_file_path, os.O_CREAT | os.O_RDWR, 0o600)
            with open(fp, "w") as key_file:
                key_file.write(downloaded_ssh_keys[key])
                downloaded_ssh_keys[key] = key_file_path
                print("- New SSH key cached at: {}".format(key_file_path))
        except Exception as exc:
            print("-- Error getting Ansible SSH keys from salt-ssh: {}".format(exc))
            exit(1)

# Tailor local Ansible Inventory to pass the right path to local cached SSH keys
def _process_node_and_fix_ssh_keys(node):
    for i in node.keys():
        if isinstance(node[i], dict):
            if node[i].keys():
                _process_node_and_fix_ssh_keys(node[i])
        elif i == 'ansible_ssh_private_key_file':
            node[i] = downloaded_ssh_keys[node[i]]

_process_node_and_fix_ssh_keys(inventory)

# Connect to SUSE Manager XMLRPC API and import missing Ansible systems
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

print("* Processing Ansible inventory")
for host in ansible_hosts:
    systems_list = client.system.listSystems(key)
    if any([host in x['name'] for x in systems_list]):
        print("- Ansible host '{}' is already imported".format(host))
    else:
        new_sys = client.system.createSystemProfile(key,
                                                    host, {"hwAddress": "fake-{}".format(host),
                                                    "host": host,
                                                    "minionId": host})
        try:
            client.system.setDetails(key, new_sys, {
                "profile_name": host,
                "base_entitlement": "foreign_entitled",
            })
            client.system.upgradeEntitlement(key, new_sys, "ansible_entitled")
            print("- New Ansible host '{}' successfully imported! ({})".format(host, new_sys))
        except Exception as exc:
            print("-- Error while setting entitlements: {}".format(exc))
            client.system.deleteSystem(key, new_sys)

# Logging out
client.auth.logout(key)

# Save Ansible Inventory locally
with open(os.path.join(LOCAL_ANSIBLE_CACHE, "ansible-inventory.yaml"), "w") as inventory_file:
    inventory_file.write(yaml.dump(inventory))
print("* Saved Ansible Inventory at: {}".format(os.path.join(LOCAL_ANSIBLE_CACHE, "ansible-inventory.yaml")))

# Done
print("* Done!")
