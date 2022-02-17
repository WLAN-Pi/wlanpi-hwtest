# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import is_module_present, run_command


def test_gpio_fan_mod():
    """
    Test command:
        lsmod | grep gpio_fan

    Results:
        True - gpio_fan module detected in lsmod
        False - not detected
    """

    assert is_module_present("gpio_fan") is True


def test_gpio_fan_conf():
    """
    Test command:
        read /boot/config.txt

    Results:
        True - "gpio-fan" exists in config.txt
        False - "gpio-fan" not found in config.txt
    """

    with open("/boot/config.txt", "r") as f:
        config_lines = f.readlines()

    results = [r for r in config_lines if "gpio-fan" in r]

    enabled = False

    for r in results:
        slice_comment = r.split("#")[0]
        if "gpio-fan" in slice_comment:
            enabled = True
            return

    assert enabled


def test_fan_detected():
    """
    Test command: sensors

    Output:
        gpio_fan-isa-0000
        Adapter: ISA adapter
        fan1:        5000 RPM  (min =    0 RPM, max = 5000 RPM)

    Expects 1:
        True - gpio_fan-isa-0000 in response
        False - did not find gpio_fan-isa-0000 in response

    Expects 2)
        True - fan0 or fan1 in the output
        False - fan0 or fan1 NOT in output

    Depends:
        sudo apt install lm-sensors
    """

    resp = run_command(["sensors"])

    assert "gpio_fan-isa-0000" in resp
    assert "fan0" or "fan1" in resp
