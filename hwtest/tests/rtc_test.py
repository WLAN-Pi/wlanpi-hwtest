from hwtest.tests.helpers import is_module_present, run_command


def test_rtc_pcf85063_module_present():
    """
    Test command:
        lsmod | grep rtc_pcf85063

    Results:
        True - rtc_pcf85063 module detected in lsmod
        False - not detected
    """

    assert is_module_present("rtc_pcf85063") == True


def test_rtc_clock_tick():
    """
    Test command:
        hwclock -v

    Expect:
        "got clock tick" in resp
    """

    resp = run_command(["hwclock", "-v"])

    assert "got clock tick" in resp.lower()
