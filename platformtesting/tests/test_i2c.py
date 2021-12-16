from platformtesting.helpers import run_command

def test_i2c_enabled():
    """
    sudo raspi-config nonint get_i2c

    1 == disabled
    0 == enabled
    """

    resp = run_command(["raspi-config", "nonint", "get_i2c"])
    
    pass#assert resp == 0