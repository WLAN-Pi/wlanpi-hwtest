from hwtest.helpers import run_command
from hwtest.tests.helpers import is_module_present


def test_i2c_module_present():
    """
    Test command:
        lsmod | grep i2c

    Results:
        True - i2c module(s) detected in lsmod
        False - not detected
    """

    assert is_module_present("i2c") == True


# enable i2c: sudo raspi-config nonint do_i2c 0
# disable i2c: sudo raspi-config nonint do_i2c 1


def test_i2c_enabled():
    """
    Test command:
        sudo raspi-config nonint get_i2c

    Expect:
        0 = i2c is enabled
        1 = i2c is disabled
    """

    resp = run_command(["raspi-config", "nonint", "get_i2c"])

    assert resp == "0"
