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


def get_ip_data(intf) -> NetworkInterface:
    # Get json output from `ip` command
    result = run_command(["ip", "-json", "address"])
    data = json.loads(result)
    # Create dict of dicts for easier assignment
    interface_data = {}
    for item in data:
        name = item["ifname"]
        interface_data[name] = item
    # Build dataclass for storage and easier test assertion
    dobj = NetworkInterface()
    if intf in interface_data.keys():
        dobj.operstate = interface_data[intf]["operstate"]
        dobj.ifname = interface_data[intf]["ifname"]
        dobj.mac = interface_data[intf]["address"]
        dobj.mtu = int(interface_data[intf]["mtu"])
        dobj.ipv4_addr = interface_data[intf]["addr_info"][0]["local"]
        dobj.ipv4_prefix = int(interface_data[intf]["addr_info"][0]["prefixlen"])
    if "usb0" not in intf:
        dobj.duplex = run_command(["cat", f"/sys/class/net/{intf}/duplex"])
        dobj.speed = int(run_command(["cat", f"/sys/class/net/{intf}/speed"]))
    return dobj


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
