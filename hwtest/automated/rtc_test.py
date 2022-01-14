from hwtest.shell_utils import is_module_present, run_command


def test_rtc_pcf85063_mod():
    """
    Test command:
        lsmod | grep rtc_pcf85063

    Results:
        True - rtc_pcf85063 module detected in lsmod
        False - not detected
    """

    assert is_module_present("rtc_pcf85063") == True


def test_rtc0_exists():
    """
        Test command:
        ls /dev/rtc0

    Expect:
        exit value is 0 (/dev/rtc0 exists)

    Not Expected:
        exit value is 2 (/dev/rtc0 does not exist)
    """

    exit_value = run_command(["ls", "/dev/rtc0"], return_exit_values=True)

    assert exit_value == 0

################
# INVALID TEST #
################
# def test_rtc_hwclock():
#     """
#     Test command:
#         hwclock -r
#
#     Expect:
#         exit value is 0 (we got a timestamp)
#
#     Not Expected:
#         exit value is 1 (cannot access hardware clock for example)
#     """
#
#     exit_value = run_command(["hwclock", "-r"], return_exit_values=True)
#
#     assert exit_value == 0
