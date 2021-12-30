# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.hwtest
~~~~~~~~~~~~~~~~~~~~

OK, let's test stuff.
"""


import inspect
import logging
import os
from datetime import datetime
from typing import Dict

import pytest
from pytest_jsonreport.plugin import JSONReport

import hwtest.cfg as cfg
from hwtest.oled import init_oled_luma_terminal, print_term_icon_and_message

# prevent pytest from creating cache files
sys.dont_write_bytecode = True

cfg.RUNNING = True


def start():
    """Call pytest from our code"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("hwtest pid is %s", os.getpid())

    try:
        oled = cfg.CONFIG.get("GENERAL").get("oled")
        verbose = cfg.CONFIG.get("GENERAL").get("verbose")
        if oled:
            import hwtest.buttons as btn  # fmt: skip

            # init oled
            init_oled_luma_terminal()
            cfg.TERMINAL.println("# START AUTO TESTS")

        automated_report = run_automated_pytests()

        if oled:
            print_term_pytest_report(automated_report, verbose=verbose)
            cfg.TERMINAL.println("# DONE AUTO TESTS")

            cfg.TERMINAL.println("# START I/A TESTS")
            interactive_report = run_interactive_pytests()
            print_term_pytest_report(interactive_report, verbose=verbose)
            cfg.TERMINAL.println("# DONE I/A TESTS")

            cfg.TERMINAL.println("-------RESULTS-------")
            print_term_pytest_summary(automated_report.get("summary"), "AUTO")
            print_term_pytest_summary(interactive_report.get("summary"), "I/A")

        cfg.BUTTON_TEST_IN_PROGRESS = False

        # keep main thread up until stopped by sigint or something else
        while cfg.RUNNING:
            pass
    except KeyboardInterrupt:
        if cfg.TERMINAL:
            cfg.TERMINAL.clear()
        cfg.RUNNING = False
        log.info("detected Control-C ... exiting ...")


def now():
    """yyyy-MM-ddThhmmss (1980-12-01T221030"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")


def run_automated_pytests() -> Dict:
    """run the automated tests"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("starting automated pytest driver")

    here = os.path.abspath(os.path.dirname(__file__))

    json_plugin = JSONReport()
    pytest.main(
        [
            "--json-report-file=none",
            "--self-contained-html",
            "--cache-clear",
            f"--html=/var/log/wlanpi-hwtest/report_automated_{now()}.html",
            "-s",
            f"{os.path.join(here, 'automated')}",
            # f"{os.path.join(here, 'automated', 'spi_test.py')}",
        ],
        plugins=[json_plugin],
    )

    return json_plugin.report


def run_interactive_pytests() -> Dict:
    """run the automated tests"""
    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("starting interactive pytest driver")

    here = os.path.abspath(os.path.dirname(__file__))

    json_plugin = JSONReport()
    pytest.main(
        [
            "--json-report-file=none",
            "--self-contained-html",
            "--cache-clear",
            f"--html=/var/log/wlanpi-hwtest/report_interactive_{now()}.html",
            "-s",
            f"{os.path.join(here, 'interactive')}",
        ],
        plugins=[json_plugin],
    )

    return json_plugin.report


def format_pytest_outcome(outcome: str) -> str:
    """format outcome for brevity"""
    return outcome.strip().upper().replace("PASSED", "PASS").replace("FAILED", "FAIL")


def format_pytest_nodeid(test_name: str) -> str:
    """format nodeid for brevity"""
    if test_name and "::" in test_name:
        return test_name.strip().split("::")[1].upper().replace("TEST_", "")
    return test_name


def print_term_pytest_report(report: Dict, verbose=False) -> None:
    reordered = sorted(report.get("tests"), key=lambda d: d["outcome"], reverse=True)

    for test in reordered:
        icon = ""
        outcome = format_pytest_outcome(test.get("outcome", ""))
        if outcome == "PASS":
            icon = "\uf058"  # fa check-circle
            if not verbose:
                continue
        if outcome == "FAIL":
            icon = "\uf00d"  # fa times
        if outcome == "ERROR":
            icon = "\uf071"  # fa exclamation-triangle
        nodeid_stub = format_pytest_nodeid(test.get("nodeid", ""))

        print_term_icon_and_message(icon, nodeid_stub, animate=True)


def print_term_pytest_summary(summary: Dict, type: str) -> None:
    ok = summary.get("passed", 0)
    fail = summary.get("failed", 0)
    error = summary.get("error", 0)
    total = summary.get("total", 0)
    if fail == total:
        # f00d https://fontawesome.com/v5.15/icons/times?style=solid
        print_term_icon_and_message("\uf00d", f"0% {type.upper()} PASS")
    elif fail > 0:
        # f00d https://fontawesome.com/v5.15/icons/times?style=solid
        print_term_icon_and_message(
            "\uf00d", f"{(total-fail)/total:.0%} {type.upper()} PASS"
        )
    if error > 0:
        # f071 https://fontawesome.com/v5.15/icons/exclamation-triangle?style=solid
        cfg.TERMINAL.println(f"{error} {type.upper()} ERRORS")
    if ok == total:
        # f058 https://fontawesome.com/v5.15/icons/check-circle
        print_term_icon_and_message("\uf058", f"100% {type.upper()} PASS")
