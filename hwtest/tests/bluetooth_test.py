from hwtest.tests.helpers import is_module_present, run_command


def test_bt_mod():
    """
    Test command:
        lsmod | grep bluetooth

    Results:
        True - bluetooth module detected in lsmod
        False - not detected
    """

    assert is_module_present("bluetooth") == True


def test_bt_device_present():
    """
    Test command:
        hciconfig | grep hci*

    Results:
        True - Bluetooth adapter(s) detected
        False - no Bluetooth adapter(s) detected
    """
    # Use hciconfig here as it works OK when no devices are present

    resp = run_command(["hciconfig", "|", "grep", "hci*"])

    assert "hci" in resp
