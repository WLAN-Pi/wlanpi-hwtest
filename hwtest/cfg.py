# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : BSD-3

"""
wlanpi-hwtest.cfg
~~~~~~~~~~~~~~~~~

module for sharing conf and objects across hwtest
"""

import os

from PIL import ImageFont

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

CONFIG = {}
RUNNING = False
TESTING = False
BUTTON_TEST_IN_PROGRESS = False

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
