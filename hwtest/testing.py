# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.testing
~~~~~~~~~~~~~~~~~~~~~

OK, let's test stuff.
"""


import argparse
import inspect
import logging
import os
import sys

import pytest


def are_we_root() -> bool:
    """Do we have root permissions?"""
    if os.geteuid() == 0:
        return True
    else:
        return False


def start(args: argparse.Namespace):
    """Call pytest from our code"""
    log = logging.getLogger(inspect.stack()[0][3])

    if not are_we_root():
        log.error(
            "application requires elevated permissions ... try running with sudo ... exiting ..."
        )
        sys.exit(-1)

    here = os.path.abspath(os.path.dirname(__file__))

    log.debug("hwtest is located in %s", here)

    retcode = pytest.main([f"{here}"])

    # we can pass in plugins like this:
    # retcode = pytest.main(["-qq"], plugins=[MyPlugin()])

    line = len(str(retcode))
    print()
    print("#" * line)
    print(retcode)
    print("#" * line)
