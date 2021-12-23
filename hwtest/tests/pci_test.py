import pytest

from hwtest.tests.helpers import run_command

# fmt: off
EXPECTED_PCI = [
    ('00:00.0', 'Broadcom Inc. and subsidiaries BCM2711 PCIe Bridge'),
    ('01:00.0', 'Pericom Semiconductor PI7C9X2G404 EL/SL PCIe2 4-Port/4-Lane Packet Switch'),
    ('03:00.0', 'USB controller: VIA Technologies, Inc. VL805 USB 3.0 Host Controller'),
    ('04:00.0', 'Network controller: Intel Corporation Wi-Fi 6 AX210/AX211/AX411 160MHz'),
    ('05:00.0', 'Network controller: Intel Corporation Wi-Fi 6 AX210/AX211/AX411 160MHz')
]
# fmt: on


@pytest.fixture(params=EXPECTED_PCI)
def get_lspci(request):
    slot = request.param[0]
    expected = request.param[1]
    return (run_command([f"lspci -s {slot}"], invoke_shell=True), expected)


def test_pci(get_lspci):
    """
    Test command:
        lspci -s xx:xx.x

    Results:
        True - PCI slot output matches expected value from tuple
        False - PCI slot output does not expected value from tuple
    """

    cmd_output, expected = get_lspci
    print(f"cmd output: {cmd_output}")
    print(f"expected output: {expected}")

    assert expected in cmd_output
