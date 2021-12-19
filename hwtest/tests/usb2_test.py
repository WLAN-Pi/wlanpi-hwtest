from hwtest.tests.helpers import is_module_present, run_command


def test_usb2_hub():
    """
    Test for Linux Foundation 2.0 root hub in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert "1d6b:0002" in resp


def test_g_ether_module_present():
    """
    Test command:
        lsmod | grep g_ether

    Results:
        True - g_ether module detected in lsmod
        False - not detected
    """

    assert is_module_present("g_ether") == True
