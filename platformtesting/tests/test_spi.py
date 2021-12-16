from platformtesting.helpers import run_command

def test_spi_enabled():
    """
    sudo raspi-config nonint get_spi
    
    1 == disabled
    0 == enabled
    """

    resp = run_command(["raspi-config", "nonint", "get_spi"])

    assert resp == '1'