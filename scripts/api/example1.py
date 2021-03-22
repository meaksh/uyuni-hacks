#!/usr/bin/python3

import time
import xmlrpc.client as xmlrpclib

UYUNI_API_URL = "https://my-uyuni-server/rpc/api"
UYUNI_API_LOGIN = "my-uyuni-user"
UYUNI_API_PASSWORD = "my-uyuni-password"

TEST_CLIENT = "my-test-client-hostname.foo.bar"

# Connect to Uyuni XMLRPC API
client = xmlrpclib.Server(UYUNI_API_URL, verbose=0)

# Login and get session key
key = client.auth.login(UYUNI_API_LOGIN, UYUNI_API_PASSWORD)

# List registered systems
print("--- List of Systems ---")
systems_list = client.system.listSystems(key)
systems_ids = {k:v for k,v in map(lambda x: (x['name'], x['id']), systems_list)}
for system in systems_ids:
   print("* {} - {}".format(system, systems_ids[system]))
print()

print("--- Recreating systems ---")
if TEST_CLIENT in systems_ids:
   # Delete the test system if already existing in Uyuni
   print("* Deleting {}".format(TEST_CLIENT))
   client.system.deleteSystem(key, systems_ids[TEST_CLIENT])

print("* Bootstrapping {}".format(TEST_CLIENT))
client.system.bootstrap(key, TEST_CLIENT, 22, "root", "my-root-pass", "", False)

systems_list = client.system.listSystems(key)
systems_ids = {k:v for k,v in map(lambda x: (x['name'], x['id']), systems_list)}

# Wait until new system is successfully registered
while not TEST_CLIENT in systems_ids:
    print("* Waiting for system registration to complete ...")
    systems_list = client.system.listSystems(key)
    systems_ids = {k:v for k,v in map(lambda x: (x['name'], x['id']), systems_list)}
    time.sleep(2)

print("* Registration finished successfully!") 
print()

# Execute some actions on the registered system
print("--- Scheduling actions ---")
my_actions = []

print("* Schedule a highstate. TestMode = False")
my_actions.append(client.system.scheduleApplyHighstate(key, systems_ids[TEST_CLIENT], xmlrpclib.DateTime(), False))
print("* Schedule a remote execution command: \"date\" with user: root, group: root, timeout 10")
my_actions.append(client.system.scheduleScriptRun(key, [systems_ids[TEST_CLIENT]], "root", "root", 10, "date; sleep 6", xmlrpclib.DateTime()))

# Wait while actions are in progress
while [act for act in client.schedule.listInProgressActions(key) if act["id"] in my_actions]:
    print("* Waiting for the actions to be completed ...")
    time.sleep(2)

print("* Actions finished!")
print()

# Check the results from the previous actions
print("--- Checking action results ---")
for act in my_actions:
   print()
   print("* Action: {}".format(act))

   completed_systems = client.schedule.listCompletedSystems(key, act)
   failed_systems = client.schedule.listFailedSystems(key, act)

   if completed_systems:
       print("* SUCCESS: {}".format(completed_systems))
   elif failed_systems:
       print("* FAIL: {}".format(failed_systems))
   else:
       print("* Error")

client.auth.logout(key)
print()
