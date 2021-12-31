import pytest

from hwtest.shell_utils import run_command

# fmt: off
params = {
    'Slot 0': ('00:00.0', '14e4:2711'),
    'Slot 1': ('01:00.0', '12d8:2404'),
    'Slot 3': ('03:00.0', '1106:3483'),
    'Slot 4': ('04:00.0', '8086:2725'),
    'Slot 5': ('05:00.0', '8086:2725')
}
# fmt: on


@pytest.mark.parametrize(
    "slot,expected", list(params.values()), ids=list(params.keys())
)
def test_pci(slot, expected):
    """
    Test command:
        lspci -s xx:xx.x

    Results:
        True - PCI slot output matches expected value from tuple
        False - PCI slot output does not expected value from tuple
    """
    cmd_output = run_command([f"lspci -s {slot} -n"], invoke_shell=True)
    print(f"cmd output: {cmd_output}")
    print(f"expected output: {expected}")

    assert expected in cmd_output


def test_4x_PI7C9X2G404():
    """
    Test presence of 4x PI7C9X2G404 packet switches in lspci output:

    00:00.0 PCI bridge: Broadcom Inc. and subsidiaries BCM2711 PCIe Bridge (rev 20)
    01:00.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
    02:01.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
    02:02.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
    02:03.0 PCI bridge: Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch (rev 05)
    03:00.0 USB controller: VIA Technologies, Inc. VL805 USB 3.0 Host Controller (rev 01)
    04:00.0 Network controller: Intel Corporation Device 2725 (rev 1a)
    05:00.0 Network controller: Intel Corporation Device 2725 (rev 1a)
    """

    lspci = run_command(["lspci"]).upper()

    assert lspci.count("PI7C9X2G404") == 4
