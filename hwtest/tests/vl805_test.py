import shutil

from hwtest.tests.shell_utils import run_command


def test_vl805_fw():
    """
    Test: sudo vl805

    Description vl805 is a binary which outputs the version of FW for the VL805 USB 3 Controller

    Expects: VL805 FW version: 000138a1
    """
    if shutil.which("vl805") is not None:
        resp = run_command(["vl805"])

        assert "000138a1" in resp
    assert False
