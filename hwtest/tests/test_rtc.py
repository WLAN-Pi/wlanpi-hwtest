from hwtest.helpers import run_command


def test_rtc_enabled():
    """
    hwclock -v

    ???
    """

    run_command(["hwclock", "-v"])

    # assert ???
