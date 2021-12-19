from hwtest.helpers import run_command


def test_usb_hub():
    """
    Test for Linux Foundation 2.0 root hub in `lsusb` output
    """

    resp = run_command(["lsusb"])

    assert "1d6b:0002" in resp
