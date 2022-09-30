# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

"""
wlanpi-hwtest.cfg
~~~~~~~~~~~~~~~~~

module for sharing conf and objects across hwtest
"""

import logging
import os
from datetime import datetime

from PIL import ImageFont

from hwtest.automated.ethernet_test import get_ip_data
from hwtest.platform import (
    PLATFORM,
    PLATFORM_M4,
    PLATFORM_PRO,
    PLATFORM_R4,
)

LOG = logging.getLogger("cfg.py")

###########
# BUTTONS #
###########


def setup_buttons():
    global BUTTONS_PRESSED
    global BUTTONS_PRINTED
    if PLATFORM == PLATFORM_PRO:
        BUTTONS_PRESSED = {
            "BUTTON_UP": False,
            "BUTTON_DOWN": False,
            "BUTTON_LEFT": False,
            "BUTTON_RIGHT": False,
            "BUTTON_CENTER": False,
        }
    elif PLATFORM == PLATFORM_M4 or PLATFORM == PLATFORM_R4:
        BUTTONS_PRESSED = {
            "BUTTON_UP": False,
            "BUTTON_DOWN": False,
            "BUTTON_LEFT": False,
            "BUTTON_RIGHT": False,
            "BUTTON_CENTER": False,
            "BUTTON_KEY1": False,
            "BUTTON_KEY2": False,
            "BUTTON_KEY3": False,
        }
    else:
        BUTTONS_PRESSED = {}

    if PLATFORM == PLATFORM_PRO:
        BUTTONS_PRINTED = {
            "BUTTON_UP": False,
            "BUTTON_DOWN": False,
            "BUTTON_LEFT": False,
            "BUTTON_RIGHT": False,
            "BUTTON_CENTER": False,
        }
    elif PLATFORM == PLATFORM_M4 or PLATFORM == PLATFORM_R4:
        BUTTONS_PRINTED = {
            "BUTTON_UP": False,
            "BUTTON_DOWN": False,
            "BUTTON_LEFT": False,
            "BUTTON_RIGHT": False,
            "BUTTON_CENTER": False,
            "BUTTON_KEY1": False,
            "BUTTON_KEY2": False,
            "BUTTON_KEY3": False,
        }
    else:
        BUTTONS_PRINTED = {}
    # LOG.debug("BUTTONS_PRINTED: %s" % BUTTONS_PRINTED)
    # LOG.debug("BUTTONS_PRESSED: %s" % BUTTONS_PRESSED)


###########
# GENERIC #
###########


def now():
    """yyyy-MM-ddThhmmss (1980-12-01T221030"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")


def get_eth0_mac():
    """000000.111111"""
    eth0_data = get_ip_data("eth0")
    eth0_mac = eth0_data.mac.replace(":", "")
    eth0_mac = ".".join([eth0_mac[0:6], eth0_mac[6:]])
    if eth0_mac:
        return eth0_mac
    return ""


CONFIG = {}
RUNNING = False
TESTING = False
PRESSED = False
COLOR_TEST_IN_PROGRESS = False
BUTTON_TEST_IN_PROGRESS = False
START_TIME = now()
ETH0_MAC = get_eth0_mac()

########
# OLED #
########

HERE = os.path.abspath(os.path.dirname(__file__))
TERMINAL = None


def make_font(name, size):
    font_path = str(os.path.join(HERE, "fonts", name))
    return ImageFont.truetype(font_path, size)


FIRACODE = make_font("FiraCode-SemiBold.ttf", 10)
FASOLID = make_font("fa-solid-900.ttf", 14)
FAREGULAR = make_font("fa-regular-400.ttf", 14)
