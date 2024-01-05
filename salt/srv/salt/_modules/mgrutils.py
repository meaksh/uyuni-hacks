import os

REBOOT_BEACON_FLAG_FILE = "/var/cache/salt/minion/reboot_flag"


def __virtual__():
    return True

def reboot():
    with open(REBOOT_BEACON_FLAG_FILE, "w") as flag_file:
        pass
