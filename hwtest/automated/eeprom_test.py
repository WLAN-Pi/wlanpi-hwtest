# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

from hwtest.shell_utils import run_command


def test_eeprom_bootloader_version_is_up_to_date():
    """
    Test: sudo CM4_ENABLE_RPI_EEPROM_UPDATE=1 rpi-eeprom-update

    Description: check that bootloader is up to date

    Pass Example:
        BOOTLOADER: up to date
        CURRENT: Tue 25 Jan 2022 02:30:41 PM UTC (1643121041)
        LATEST: Tue 25 Jan 2022 02:30:41 PM UTC (1643121041)

        echo $? == 0

    Fail Example:
        BOOTLOADER: update available
        CURRENT: Tue 16 Feb 2021 01:23:36 PM UTC (1613481816)
        LATEST: Tue 25 Jan 2022 02:30:41 PM UTC (1643121041)

        echo $? == 1
    """

    ret_code = run_command(
        ["sudo", "CM4_ENABLE_RPI_EEPROM_UPDATE=1", "rpi-eeprom-update"],
        return_exit_values=True,
    )

    assert ret_code == 0


def test_rpi_eeprom_config_power_off_on_halt():
    """
    Test: rpi-eeprom-config

    Pass example: if POWER_OFF_ON_HALT=1 exists

    Example output:
        rpi-eeprom-config
        [all]
        BOOT_UART=0
        WAKE_ON_GPIO=0
        POWER_OFF_ON_HALT=1
        DISABLE_HDMI=1
        VL805=0

        # Try SD first (1), followed by, USB PCIe, NVMe PCIe, USB SoC XHCI then network
        BOOT_ORDER=0xf25641she

        # Set to 0 to prevent bootloader updates from USB/Network boot
        # For remote units EEPROM hardware write protection should be used.
        ENABLE_SELF_UPDATE=1
    """

    resp = run_command(["rpi-eeprom-config"])

    assert "POWER_OFF_ON_HALT=1" in resp
