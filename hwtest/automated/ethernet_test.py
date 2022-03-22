# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

import json
from dataclasses import dataclass

import pytest

from hwtest.shell_utils import run_command


@dataclass
class NetworkInterface:
    ifname: str = None
    operstate: str = None
    mac: str = None
    mtu: int = None
    duplex: str = None
    speed: int = None
    ipv4_addr: str = None
    ipv4_prefix: int = None


def get_ip_data(_iface) -> NetworkInterface:
    # Get json output from `ip` command
    result = run_command(["ip", "-json", "address"])
    data = json.loads(result)
    # Create dict of dicts for easier assignment
    interface_data = {}
    for item in data:
        name = item["ifname"]
        interface_data[name] = item

    # Build dataclass for storage and easier test assertion
    iface = NetworkInterface()

    if _iface in interface_data.keys():
        iface.operstate = interface_data.get(_iface, {}).get("operstate")
        iface.ifname = interface_data.get(_iface, {}).get("ifname")
        iface.mac = interface_data.get(_iface, {}).get("address")
        iface.mtu = int(interface_data.get(_iface, {}).get("mtu"))
    if "usb0" not in _iface:
        iface.duplex = run_command(["cat", f"/sys/class/net/{_iface}/duplex"])
        iface.speed = int(run_command(["cat", f"/sys/class/net/{_iface}/speed"]))

    return iface


@pytest.fixture()
def eth0_data():
    return get_ip_data("eth0")


def test_eth0_up(eth0_data):
    """
    Test commands:
        ip address
        cat /sys/class/net/{intf}/duplex
        cat /sys/class/net/{intf}/speed

    Results:
        True - eth0 state is "UP"
        False - any other output
    """
    assert eth0_data.operstate == "UP"
