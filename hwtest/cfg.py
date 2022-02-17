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

import os
from datetime import datetime

from PIL import ImageFont

from hwtest.automated.ethernet_test import get_ip_data

###########
# BUTTONS #
###########

BUTTONS_PRESSED = {
    "BUTTON_UP": False,
    "BUTTON_DOWN": False,
    "BUTTON_LEFT": False,
    "BUTTON_RIGHT": False,
    "BUTTON_CENTER": False,
}

BUTTONS_PRINTED = {
    "BUTTON_UP": False,
    "BUTTON_DOWN": False,
    "BUTTON_LEFT": False,
    "BUTTON_RIGHT": False,
    "BUTTON_CENTER": False,
}

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
