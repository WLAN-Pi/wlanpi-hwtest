# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import is_module_present, run_command


def test_bt_module():
    """
    Test command:
        lsmod | grep bluetooth

    Results:
        True - bluetooth module detected in lsmod
        False - not detected
    """

    assert is_module_present("bluetooth") == True


def test_2x_bt_devices():
    """
    Test command:
        hciconfig | grep hci*

    Results:
        True - (2) bluetooth adapters exist
        False - <2 or >2 bluetooth adapters exist
    """
    # Use hciconfig here as it works OK when no devices are present

    resp = run_command(["hciconfig"]).lower()

    assert resp.count("hci") == 2
    # assert resp.count("up") == 2
