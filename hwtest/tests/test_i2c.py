from hwtest.helpers import run_command


def test_i2c_enabled():
    """
    Test command:
        sudo raspi-config nonint get_i2c

    Expect:
        0 = i2c is enabled
        1 = i2c is disabled
    """

    resp = run_command(["raspi-config", "nonint", "get_i2c"])

    assert resp == 0
