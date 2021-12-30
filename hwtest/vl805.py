# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.helpers
~~~~~~~~~~~~~~~~~~~~~

provides functions which help setup the app.
"""

import inspect
import logging
import shutil
import sys
import os

import hwtest.cfg as cfg
from hwtest.shell_utils import run_command

def get_vl805_firmware_file() -> str:
    log = logging.getLogger(inspect.stack()[0][3])
    bin_file = "/opt/wlanpi-hwtest/firmware/stable/vl805_000138a1.bin"

    if not os.path.isfile(bin_file):
        log.debug("Checking development folder because cannot find %s", bin_file)
        dev_bin_file = os.path.join(cfg.HERE, "../install", bin_file[1:])
        if os.path.isfile(dev_bin_file):
            return dev_bin_file
        else:
            log.error("Cannot find %s", dev_bin_file)
    return bin_file


VL805_FIRMWARE_REVISION = "000138a1"
VL805_FILE = get_vl805_firmware_file()

def check_vl805_utility_exists() -> bool:    
    if shutil.which("vl805") is None:
        return False
    return True

def get_vl805_response() -> str:
    """ get the vl805 firmware """
    resp = run_command(["vl805"])

    return resp

def expected_vl805_firmware(vl805_resp) -> bool:
    """ is the vl805 firmware what we expect """
    if VL805_FIRMWARE_REVISION in vl805_resp:
        return True
    return False

def upgrade_vl805_firmware() -> bool:
    """ use vl805 utility to upgrade firmware

    Example:
        vl805 -w vl805_000138a1.bin
    """
    if os.path.isfile(VL805_FILE):
        retcode = run_command(["vl805", "-w", f"{VL805_FILE}"], return_exit_values=True)
        if retcode == 0:
            return True
    return False
    

def verify_vl805_firmware() -> bool:
    """ 
    use vl805 utility to verify firmware revision

    Example
        vl805 -v vl805_000138a1.bin
    """
    log = logging.getLogger(inspect.stack()[0][3])
    
    if os.path.isfile(VL805_FILE):
        resp = run_command(["vl805", "-v", f"{VL805_FILE}"])
        retcode = run_command(["vl805", "-v", f"{VL805_FILE}"], return_exit_values=True)
        if retcode == 0:
            return True
        else:
            log.error(resp)
    return False

def check_and_upgrade_firmware() -> bool:
    log = logging.getLogger(inspect.stack()[0][3])
    
    # check vl805 utility exists
    if not check_vl805_utility_exists():
        log.error("VL805 not found on path ... Exiting ...")
        sys.exit(-1)

    # get firmware
    resp = get_vl805_response()

    # if firmware is not expected we need to upgrade it
    if not expected_vl805_firmware(resp):
    
        # try upgrading to our desired version.
        if upgrade_vl805_firmware():

            # verify firmware
            if verify_vl805_firmware():
                # if upgraded, trigger reboot
                os.system("sudo reboot")
            else:
                # if not expected, halt and warn user.
                log.error("We upgraded VL805 firmware to %s, but verification failed ... Exiting ...", VL805_FIRMWARE_REVISION)
                sys.exit(-1)
        else:
            log.error("Upgrading VL805 firmware to %s failed ... Exiting ...", VL805_FIRMWARE_REVISION)
            sys.exit(-1)
    
    log.debug("VL805 is using expected firmware revision %s", VL805_FIRMWARE_REVISION)
    return True