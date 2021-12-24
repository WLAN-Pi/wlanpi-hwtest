import pytest

from hwtest.tests.helpers import run_command

params = {
    'Slot 0': ('00:00.0', 'Broadcom Inc. and subsidiaries BCM2711 PCIe Bridge'),
    'Slot 1': ('01:00.0', 'Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch'),
    'Slot 3': ('03:00.0', 'USB controller: VIA Technologies, Inc. VL805 USB 3.0 Host Controller'),
    'Slot 4': ('04:00.0', 'Network controller: Intel Corporation Wi-Fi 6 AX210/AX211/AX411 160MHz'),
    'Slot 5': ('05:00.0', 'Network controller: Intel Corporation Wi-Fi 6 AX210/AX211/AX411 160MHz')
}


@pytest.mark.parametrize('slot,expected', list(params.values()), ids=list(params.keys()))
def test_pci(slot, expected):
    """
    Test command:
        lspci -s xx:xx.x

    Results:
        True - PCI slot output matches expected value from tuple
        False - PCI slot output does not expected value from tuple
    """
    cmd_output = run_command([f"lspci -s {slot}"], invoke_shell=True)
    print(f"cmd output: {cmd_output}")
    print(f"expected output: {expected}")

    assert expected in cmd_output
