# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

"""
wlanpi-hwtest.__main__.py
~~~~~~~~~~~~~~~~~~~~~~~~~

Entry point for hwtest
"""

import os
import platform
import signal
import sys

from . import hwtest, vl805


def receiveSignal(signum, _frame):
    hwtest.cfg.RUNNING = False
    sys.exit(signum)


signal.signal(signal.SIGINT, receiveSignal)
signal.signal(signal.SIGTERM, receiveSignal)


def elevated_permissions() -> bool:
    """Do we have root permissions?"""
    if os.geteuid() == 0:
        return True
    else:
        return False


if not elevated_permissions():
    print(
        "hwtest requires elevated permissions ... try running with sudo ... exiting ..."
    )
    sys.exit(-1)


def main():
    """Set up args and start the testing suites"""
    from . import helpers

    parser = helpers.setup_parser()
    args = parser.parse_args()
    helpers.setup_logger(args)
    hwtest.cfg.CONFIG = helpers.read_config(args)

    if hwtest.cfg.CONFIG.get("GENERAL").get("firmware"):
        if vl805.check_and_upgrade_firmware():
            hwtest.start()
    else:
        hwtest.start()


def init():
    """Handle main init"""
    # hard set no support for non linux platforms
    if "linux" not in sys.platform:
        sys.exit(
            "{0} only works on Linux... exiting...".format(os.path.basename(__file__))
        )

    # hard set no support for python < v3.7
    if sys.version_info < (3, 7):
        sys.exit(
            "{0} requires Python version 3.7 or higher...\nyou are trying to run with Python version {1}...\nexiting...".format(
                os.path.basename(__file__), platform.python_version()
            )
        )

    if __name__ == "__main__":
        sys.exit(main())


init()
