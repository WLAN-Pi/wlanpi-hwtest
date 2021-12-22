from typing import List

from hwtest.tests.helpers import run_command


def _expected_lspci_resp():
    return """
00:00.0 PCI bridge: Broadcom Inc. and subsidiaries BCM2711 PCIe Bridge (rev 20)
01:00.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
02:01.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
02:02.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
02:03.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
03:00.0 USB controller: VIA Technologies, Inc. VL805 USB 3.0 Host Controller (rev 01)
04:00.0 Network controller: Intel Corporation Device 2725 (rev 1a)
05:00.0 Network controller: Intel Corporation Device 2725 (rev 1a)
    """


def lookup_lspci(target: str) -> List:
    # get lspci output
    lspci = run_command(["lspci"])

    hits = []
    target = "PI7C9X2G404"
    for line in lspci.splitlines():
        if target in line:
            hits.append(line)

    return hits


def test_PI7C9X2G404_packet_switches():
    """
    Test presence of 4x PI7C9X2G404 packet switches in lspci output
    """

    pcie_packet_switches = lookup_lspci("PI7C9X2G404")

    assert len(pcie_packet_switches) == 4


def test_vl_805_usb3_host_controller():
    """
    Test for VL805 USB 3.0 Host Controller in `lspci` output
    """

    resp = run_command(["lspci"])

    assert "VL805" in resp


def test_usb3_hub():
    """
    Test for Linux Foundation 3.0 root hub in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert "1d6b:0003" in resp
