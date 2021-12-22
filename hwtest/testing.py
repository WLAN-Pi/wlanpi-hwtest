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
from time import sleep

import pytest
from luma.core.virtual import terminal

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
RUNNING = True
DEFINITIONS = [
    ("tests/bluetooth_test.py", "test_bt_mod"),
    ("tests/bluetooth_test.py", "test_bt_device_present"),
    ("tests/rtc_test.py", "test_rtc_pcf85063_mod"),
    ("tests/rtc_test.py", "test_rtc_clock_tick"),
    ("tests/pci_test.py", "test_pci_bridge"),
    ("tests/i2c_test.py", "test_i2c_mod"),
    ("tests/i2c_test.py", "test_i2c_enabled"),
    ("tests/spi_test.py", "test_spi_enabled"),
    ("tests/spi_test.py", "test_spi_mod"),
    ("tests/usb2_test.py", "test_g_ether_mod"),
    ("tests/usb2_test.py", "test_linux_usb2hub"),
    ("tests/usb3_test.py", "test_4x_PI7C9X2G404"),
    ("tests/usb3_test.py", "test_linux_usb3hub"),
    ("tests/usb3_test.py", "test_vl805_usb3ctlr"),
]


def receiveSignal(signum, _frame):
    """Handle keyboardinterrupt"""
    print("Detected SIGINT or Control-C ...")
    global RUNNING
    RUNNING = False


signal.signal(signal.SIGINT, receiveSignal)


def start(args: argparse.Namespace):
    """Call pytest from our code"""
    log = logging.getLogger(inspect.stack()[0][3])

    if not are_we_root():
        log.error(
            "application requires elevated permissions ... try running with sudo ... exiting ..."
        )
        sys.exit(-1)

    # run all tests and generate html report for /var/log/hwtest/
    run_pytest_main()

    # run each test individually and then draw results to oled
    init_oled()
    setup_luma_terminal()
    results = run_tests()
    draw_tests(results)

    # keep main thread up until stopped by sigint or something else
    while RUNNING:
        pass


def init_oled():
    """init our oled object"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("oled.init")
    oled.init()


def setup_luma_terminal():
    """draw terminal test"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("draw_terminal")
    device = oled.device
    global TERMINAL
    TERMINAL = terminal(device)


def run_tests():
    results = []
    counter = 0
    TERMINAL.println(f"WLANPI HWTEST {__version__}")
    global DEFINITIONS
    for test in DEFINITIONS:
        counter += 1
        TERMINAL.puts(
            "\rRUNNING TESTS: {}%".format(int(counter / len(DEFINITIONS) * 100))
        )
        TERMINAL.flush()
        results.append(perform_tests(test[0], test[1]))
    sleep(1)
    TERMINAL.clear()

    results.sort(reverse=True)
    return results


def format_exit_code(exit_code: str) -> str:
    return (
        exit_code.strip()
        .replace("ExitCode.", "")
        .replace("TESTS_", "")
        .replace("FAILED", "FAIL")
        .replace("_ERROR", "")
    )


def format_test_out(test: str) -> str:
    return test.strip().replace("test_", "")


def perform_tests(file: str, test: str):
    retcode = pytest.main([f"{HERE}/{file}::{test}"])
    result = format_exit_code(str(retcode))
    test = format_test_out(test)
    return (result, test)


def draw_tests(test_results):
    totals = {}
    counter = 0
    for test in test_results:
        counter += 1
        result = test[0]
        name = test[1]
        if result not in totals.keys():
            totals[result] = 1
        else:
            totals[result] += 1
        draw(f"{result}: {name}")

    fail_count = int(totals.get("FAIL", 0))
    ok_count = int(totals.get("OK", 0))
    usage_count = int(totals.get("USAGE", 0))
    if fail_count > 0:
        draw(f"{fail_count} OF {counter} FAILED!")
    elif ok_count == counter:
        draw(f"ALL {counter} TESTS PASSED")
    else:
        draw("WARNING!")
        draw(f"ONLY {ok_count} OF {counter} OK")
        draw(f"{usage_count} OF {counter} HAVE PYTEST USAGE ERROR")


def draw(out, empty_line_after=False):
    TERMINAL.println(out)
    if empty_line_after:
        TERMINAL.println()


def now():
    """yyyy-MM-ddThhmmss (1980-12-01T221030"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")


def run_pytest_main():
    logging.getLogger(inspect.stack()[0][3])

    here = os.path.abspath(os.path.dirname(__file__))

    pytest.main(
        [
            "--self-contained-html",
            f"--html=/var/log/hwtest/report_{now()}.html",
            f"{here}",
        ]
    )
