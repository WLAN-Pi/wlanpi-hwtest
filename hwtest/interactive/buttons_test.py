# -*- coding: utf-8 -*-


import inspect
import logging
import signal

import pytest

import hwtest.cfg as cfg


@pytest.fixture(scope="session", autouse=True)
def term_handler():
    orig = signal.signal(signal.SIGTERM, signal.getsignal(signal.SIGINT))
    yield
    signal.signal(signal.SIGTERM, orig)


def all_expected_buttons_pressed() -> bool:
    return all(value == True for value in cfg.BUTTONS_PRESSED.values())


def test_5x_buttons():
    log = logging.getLogger(inspect.stack()[0][3])
    cfg.BUTTON_TEST_IN_PROGRESS = True

    if cfg.CONFIG.get("GENERAL").get("oled"):
        cfg.TERMINAL.println("PRESS ALL 5 BUTTONS")
        cfg.TERMINAL.animate = False
    else:
        log.info("PRESS ALL BUTTONS TO CONTINUE")

    try:
        while cfg.RUNNING:
            if all_expected_buttons_pressed():
                break
    except KeyboardInterrupt:
        pass

    if all_expected_buttons_pressed():
        log.info("ALL EXPECTED BUTTONS HAVE BEEN PRESSED")

    cfg.BUTTON_TEST_IN_PROGRESS = False

    assert all_expected_buttons_pressed() == True
