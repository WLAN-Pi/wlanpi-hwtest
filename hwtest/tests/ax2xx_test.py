from hwtest.tests.helpers import run_command


def ax2xx_devices_present_lspci():
    """
    Test command:
        lspci | grep Intel

    Results:
        True - (2) network controllers of "Intel Corporation Wi-Fi 6" exist
        False - <2 or >2 network controllers of "Intel Corporation Wi-Fi 6" exist
    """
    resp = run_command(["lspci", "|", "grep", "Intel"])

    assert resp.count('Intel Corporation Wi-Fi 6') == 2


def ax2xx_devices_present_iw():
    """
    Test command:
        iw dev

    Results:
        True - (>=2) "#phys" are seen and (2) instances of "1c:99:57" are seen
        False - <2 "#phys" are seen or (2) instances of "1c:99:57" are not seen
    """
    resp = run_command(["iw", "dev"])

    assert resp.count('phy#') >= 2
    assert resp.count('1c:99:57') == 2
