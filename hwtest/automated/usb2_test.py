# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import is_module_present, run_command


def test_linux_usb2hub():
    """
    Test for Linux Foundation 2.0 root hub in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert "1d6b:0002" in resp


def test_g_ether_mod():
    """
    Test command:
        lsmod | grep g_ether

    Results:
        True - g_ether module detected in lsmod
        False - not detected
    """

    assert is_module_present("g_ether") == True
