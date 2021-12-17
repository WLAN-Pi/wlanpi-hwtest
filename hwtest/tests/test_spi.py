from hwtest.helpers import run_command


def test_spi_enabled():
    """
    Test command:
        sudo raspi-config nonint get_spi

    Expect:
        0 = SPI is enabled
        1 = SPI is disabled
    """

    resp = run_command(["raspi-config", "nonint", "get_spi"])

    assert resp == "0"
