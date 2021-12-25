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
import signal
import sys
from datetime import datetime
from typing import Dict

import pytest
from luma.core.virtual import terminal
from PIL import ImageFont
from pytest_jsonreport.plugin import JSONReport

from . import oled
from .__version__ import __version__


def are_we_root() -> bool:
    """Do we have root permissions?"""
    if os.geteuid() == 0:
        return True
    else:
        return False


HERE = os.path.abspath(os.path.dirname(__file__))
TERMINAL = None
EMULATE = False
RUNNING = False
TESTING_IN_PROGRESS = False
DEFINITIONS = []


@pytest.fixture(scope="session", autouse=True)
def term_handler():
    orig = signal.signal(signal.SIGTERM, signal.getsignal(signal.SIGINT))
    yield
    signal.signal(signal.SIGTERM, orig)
    TERMINAL.clear()


def start(args: argparse.Namespace):
    """Call pytest from our code"""
    log = logging.getLogger(inspect.stack()[0][3])

    if not are_we_root():
        log.error(
            "application requires elevated permissions ... try running with sudo ... exiting ..."
        )
        sys.exit(-1)

    global RUNNING
    RUNNING = True

    global TESTING_IN_PROGRESS
    TESTING_IN_PROGRESS = True

    # emulate keyboard pressing (disables detection of real button presses)
    if args.emulate:
        global EMULATE
        EMULATE = True

    init_oled()
    init_luma_terminal()
    try:

        report = run_pytest()
        TESTING_IN_PROGRESS = False
        print_pytest_outcomes(report.get("tests"))
        TERMINAL.println("-" * TERMINAL.width)
        print_pytest_summary(report.get("summary"))

        # keep main thread up until stopped by sigint or something else
        while RUNNING:
            pass
    except KeyboardInterrupt:
        TERMINAL.clear()
        RUNNING = False
        log.info("detected Control-C ... exiting ...")


def init_oled():
    """initialize our oled object"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("oled.init()")
    oled.init()


def make_font(name, size):
    font_path = str(os.path.join(HERE, "fonts", name))
    return ImageFont.truetype(font_path, size)


FIRACODE = make_font("FiraCode-SemiBold.ttf", 10)
FASOLID = make_font("fa-solid-900.ttf", 15)
FAREGULAR = make_font("fa-regular-400.ttf", 15)


def init_luma_terminal():
    """initialize terminal test"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("init oled terminal")
    device = oled.device
    global TERMINAL

    TERMINAL = terminal(
        device, FIRACODE, color="white", bgcolor="black", line_height=15
    )
    TERMINAL.println(f"WLANPI HWTEST {__version__}")
    TERMINAL.println("Starting tests ...")


def now():
    """yyyy-MM-ddThhmmss (1980-12-01T221030"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")


def run_pytest() -> Dict:
    """run the pytest driver"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("starting pytest driver")

    here = os.path.abspath(os.path.dirname(__file__))

    json_plugin = JSONReport()
    pytest.main(
        [
            "--json-report-file=none",
            "--self-contained-html",
            f"--html=/var/log/hwtest/report_{now()}.html",
            "-s",
            f"{here}",
        ],
        plugins=[json_plugin],
    )

    return json_plugin.report


def format_pytest_outcome(outcome: str) -> str:
    """format outcome for brevity"""
    return outcome.strip().upper().replace("PASSED", "PASS").replace("FAILED", "FAIL")


def format_pytest_nodeid(test_name: str) -> str:
    """format nodeid for brevity"""
    return test_name.strip().split("::")[1].upper().replace("TEST_", "")


def iconized_print(icon, message, icon_font=FASOLID):
    TERMINAL.font = icon_font
    TERMINAL.puts(f"{icon}")
    TERMINAL.font = FIRACODE
    TERMINAL.puts(f" {message}\n")
    TERMINAL.flush()


def print_pytest_outcomes(tests):
    """sort outcomes in reverse and print to oled"""
    reordered = sorted(tests, key=lambda d: d["outcome"], reverse=True)

    for test in reordered:
        outcome = format_pytest_outcome(test.get("outcome", ""))
        if outcome == "PASS":
            outcome = "\uf058"  # fa check-circle
        if outcome == "FAIL":
            outcome = "\uf00d"  # fa times
        nodeid_stub = format_pytest_nodeid(test.get("nodeid", ""))
        iconized_print(outcome, nodeid_stub)


def print_pytest_summary(summary):
    """print pytest summary to oled"""
    ok = summary.get("passed", 0)
    fail = summary.get("failed", 0)
    total = summary.get("total", 0)
    if fail > 0:
        TERMINAL.println(f"{fail} OF {total} FAILED!")
    if ok == total:
        TERMINAL.println(f"ALL {total} TESTS PASS")
