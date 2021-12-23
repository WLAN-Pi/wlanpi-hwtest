from hwtest.tests.helpers import is_module_present


def test_gpio_module():
    """
    Test command:
        lsmod | grep gpio_fan

    Results:
        True - gpio_fan module detected in lsmod
        False - not detected
    """

    assert is_module_present('gpio_fan') is True


def test_gpio_config():
    """
    Test command:
        read /boot/config.txt

    Results:
        True - "gpio-fan" exists in config.txt
        False - "gpio-fan" not found in config.txt
    """

    with open('/boot/config.txt', 'r') as f:
        config_txt = f.read()
        assert 'gpio-fan' in config_txt
