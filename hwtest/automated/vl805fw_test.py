import shutil

from hwtest.vl805 import VL805_FIRMWARE_REVISION
from hwtest.shell_utils import run_command


def test_vl805_fw():
    """
    Test: sudo vl805

    Description vl805 is a binary which outputs the version of FW for the VL805 USB 3 Controller

    Expects: VL805 FW version: 000138a1
    """
    if shutil.which("vl805") is not None:
        resp = run_command(["vl805"])

    assert VL805_FIRMWARE_REVISION in resp
