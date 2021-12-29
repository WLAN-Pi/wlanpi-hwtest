# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.__main__.py
~~~~~~~~~~~~~~~~~~~~~~~~~

Entry point
"""

import os
import platform
import sys

from . import hwtest


def main():
    """Set up args and start the testing suites"""
    from . import helpers

    parser = helpers.setup_parser()
    args = parser.parse_args()
    helpers.setup_logger(args)

    hwtest.start(args)


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
