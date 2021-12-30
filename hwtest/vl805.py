# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : BSD-3

"""
wlanpi-hwtest.helpers
~~~~~~~~~~~~~~~~~~~~~

provides functions which help setup the app.
"""

import inspect
import logging
import os
import shutil
import sys

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
    """get the vl805 firmware"""
    resp = run_command(["vl805"])

    return resp


def expected_vl805_firmware(vl805_resp) -> bool:
    """is the vl805 firmware what we expect"""
    log = logging.getLogger(inspect.stack()[0][3])
    if VL805_FIRMWARE_REVISION in vl805_resp:
        log.info("firmware revision is %s", VL805_FIRMWARE_REVISION)
        return True
    log.warning(
        "firmware revision %s not found in VL805 response", VL805_FIRMWARE_REVISION
    )
    return False


def upgrade_vl805_firmware() -> bool:
    """use vl805 utility to upgrade firmware

    Example:
        vl805 -w vl805_000138a1.bin
    """
    log = logging.getLogger(inspect.stack()[0][3])
    if os.path.isfile(VL805_FILE):
        retcode = run_command(["vl805", "-w", f"{VL805_FILE}"], return_exit_values=True)
        if retcode == 0:
            log.info("Success writing %s to EEPROM", VL805_FILE.split("/")[-1])
            return True
    log.warning("Problem writing %s to EEPROM", VL805_FILE.split("/")[-1])
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
            log.info("%s EEPROM data verified", VL805_FILE.split("/")[-1])
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

    # if firmware is not expected we need to upgrade it
    if not verify_vl805_firmware():

        log.info("Upgrading VL805 EEPROM")
        # try upgrading to our desired version.
        if upgrade_vl805_firmware():

            # verify firmware
            if verify_vl805_firmware():
                log.info("Rebooting to activate verified and reprogrammed EEPROM")

                # if upgraded, trigger reboot
                os.system("sudo reboot")
            else:
                # if not expected, halt and warn user.
                log.error(
                    "We upgraded VL805 firmware to %s, but verification failed ... Exiting ...",
                    VL805_FIRMWARE_REVISION,
                )
                sys.exit(-1)
        else:
            log.error(
                "Upgrading VL805 firmware to %s failed ... Exiting ...",
                VL805_FIRMWARE_REVISION,
            )
            sys.exit(-1)

    log.debug("VL805 is using expected firmware revision (%s)", VL805_FIRMWARE_REVISION)
    return True
