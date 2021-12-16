from platformtesting.helpers import run_command

def test_rtc_enabled():
    """
    hwclock -v

    ???
    """

    resp = run_command(["hwclock", "-v"])

    #assert ??? 
    pass