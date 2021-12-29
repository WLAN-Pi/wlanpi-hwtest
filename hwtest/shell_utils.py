# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.shell_utils
~~~~~~~~~~~~~~~~~~~~~~~~~

provides functions which help provide consistency across tests
"""

import subprocess


def is_module_present(module: str) -> bool:
    """
    Use modinfo to check if a provided module is loaded

    If output is found, return True.

    If no output is found, return False.
    """
    try:
        cmd = f"lsmod | grep {module}"
        subprocess.check_output(cmd, shell=True)
        return True
    except subprocess.CalledProcessError as _error:
        return False


def run_command(
    cmd: list, suppress_output=False, return_exit_values=False, invoke_shell=False
) -> str:
    """Run a single CLI command with subprocess and return stdout or stderr response"""
    cp = subprocess.run(
        cmd,
        encoding="utf-8",
        shell=invoke_shell,
        check=False,
        capture_output=True,
    )

    if return_exit_values:
        return cp.returncode

    if not suppress_output:
        if cp.stdout:
            return cp.stdout.strip()
        if cp.stderr:
            return cp.stderr.strip()

    return "completed process return code is non-zero with no stdout or stderr"
