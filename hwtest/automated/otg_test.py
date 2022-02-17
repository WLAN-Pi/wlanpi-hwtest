# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import is_module_present, run_command

# Further reading: https://michael.stapelberg.ch/posts/2021-04-27-linux-usb-virtual-serial-cdc-acm/


def test_RNDIS_gadget():
    """
    Test for idProduct 0xa4a2 Linux-USB Ethernet/RNDIS Gadget in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert ":a4a2 " in resp
    assert "RNDIS" in resp


def test_cdc_ether_mod():
    """
    Test command:
        lsmod | grep cdc_ether

    Results:
        True - cdc_ether module detected in lsmod
        False - not detected

    Description:
        g_ether is used on the device/peripheral side, cdc_ether is used on the host side.

        If we see cdc_ether loaded then we know communication is established between the 2 USB ports.
    """

    assert is_module_present("cdc_ether") == True
