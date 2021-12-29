from hwtest.shell_utils import run_command


def test_bq27546_exists():
    """
    Command: ls -l /sys/class/power_supply/bq27546-0

    Results:
        Exit code 0 if valid
        Exit code 127 if no such file or directory
    """
    resp = run_command(
        ["ls", "-l", "/sys/class/power_supply/bq27546-0"], return_exit_values=True
    )

    assert resp == 0
