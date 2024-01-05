import datetime
import os
import logging

log = logging.getLogger(__name__)

__virtualname__ = "mgrtransactional_reboot"


def validate(config):
    """
    Validate the config is a dict
    """
    if not isinstance(config, dict):
        return False, "Configuration for mgrtransactional_reboot beacon must be a dict."
    if not config.get("flag_file"):
        return False, "Configuration for mgrtransactional_reboot must contain 'flag_file' attribute."
    return True, "Valid beacon configuration"


def __virtual__():
    return __virtualname__


def beacon(config):
    """
    Return event in case file exist
    """
    ctime = datetime.datetime.utcnow().isoformat()

    if not os.path.isfile(config["flag_file"]):
        return []

    try:
        os.remove(config["flag_file"])
    except IOError as exc:
        log.error("Error when writting file {}: {}".format(config["flag_file"], exc))

    return [{"tag": ctime, "data": "system reboot requested"}]
