# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import is_module_present, run_command


def test_spi_mod():
    """
    Test command:
        lsmod | grep spi_bcm

    Results:
        True - spi_bcm* module detected in lsmod
        False - not detected
    """

    assert is_module_present("spi_bcm") == True


def test_spi_enabled():
    """
    Test command:
        sudo raspi-config nonint get_spi

    Expect:
        0 = SPI is enabled
        1 = SPI is disabled
    """

    resp = run_command(["raspi-config", "nonint", "get_spi"])

    assert resp == "0"
