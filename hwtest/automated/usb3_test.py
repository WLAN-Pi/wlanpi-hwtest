from hwtest.shell_utils import run_command


def test_linux_usb3hub():
    """
    Test for Linux Foundation 3.0 root hub in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert "1d6b:0003" in resp
