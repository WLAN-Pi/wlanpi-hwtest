# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

"""
wlanpi-hwtest.buttons
~~~~~~~~~~~~~~~~~~~~~

button handling code
"""

import inspect
import logging
import os
import sys
import termios
import threading
import tty

from gpiozero import Button as GPIO_Button
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

import hwtest.cfg as cfg
from hwtest.oled import print_term_icon_and_message
from hwtest.platform import (PLATFORM_M4, PLATFORM_PRO, PLATFORM_R4,
                             PLATFORM_UNKNOWN)

# Button mapping for the WLAN Pi Pro v1 Rev1
BUTTONS_WLANPI_PRO_V1_REV1 = {
    "up": 22,
    "down": 15,
    "left": 17,
    "right": 27,
    "center": 14,
}

# Button mapping for the WLAN Pi Pro v1 Rev2
BUTTONS_WLANPI_PRO_V1_REV2 = {
    "up": 22,
    "down": 5,
    "left": 17,
    "right": 27,
    "center": 6,
}

# Button mapping for the Waveshare 1.44 inch LCD Display HAT
# https://www.waveshare.com/1.44inch-lcd-hat.htm
BUTTONS_WAVESHARE = {
    "up": 6,
    "down": 19,
    "left": 5,
    "right": 26,
    "center": 13,
    "key1": 21,
    "key2": 20,
    "key3": 16,
}

PINS = {}

LOG = logging.getLogger("buttons.py")
LOG.debug("cfg.PLATFORM is %s" % cfg.PLATFORM)
if cfg.PLATFORM == PLATFORM_R4:
    PINS = BUTTONS_WAVESHARE
    LOG.debug("Using buttons for Waveshare (R4/M4)")
else:
    PINS = BUTTONS_WLANPI_PRO_V1_REV2
    LOG.debug("Using buttons for PRO V1 REV2")


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def button_emulation():
    log = logging.getLogger(inspect.stack()[0][3])
    while cfg.RUNNING:
        char = getch()
        log.debug(f"getch() detected {char}")

        if char == "k" or char == "K":
            log.info(
                "Button emulation stop requested ... Killing button emulation ... Press CTRL-C to exit ..."
            )
            break

        if char == PINS.get("up") or char == "w":
            log.info("EMULATE BUTTON UP PRESS")
            BUTTON_UP.pin.drive_low()
            BUTTON_UP.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_UP"] = True

        if char == PINS.get("down") or char == "x":
            log.info("EMULATE BUTTON DOWN PRESS")
            BUTTON_DOWN.pin.drive_low()
            BUTTON_DOWN.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_DOWN"] = True

        if char == PINS.get("left") or char == "a":
            log.info("EMULATE BUTTON LEFT PRESS")
            BUTTON_LEFT.pin.drive_low()
            BUTTON_LEFT.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_LEFT"] = True

        if char == PINS.get("right") or char == "d":
            log.info("EMULATE BUTTON RIGHT PRESS")
            BUTTON_RIGHT.pin.drive_low()
            BUTTON_RIGHT.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_RIGHT"] = True

        if char == PINS.get("center") or char == "s":
            log.info("EMULATE BUTTON CENTER PRESSED")
            BUTTON_CENTER.pin.drive_low()
            BUTTON_CENTER.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_CENTER"] = True

        if char == PINS.get("key1") or char == "1":
            log.info("EMULATE BUTTON KEY1 PRESSED")
            BUTTON_KEY1.pin.drive_low()
            BUTTON_KEY1.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_KEY1"] = True

        if char == PINS.get("key2") or char == "1":
            log.info("EMULATE BUTTON KEY2 PRESSED")
            BUTTON_KEY2.pin.drive_low()
            BUTTON_KEY2.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_KEY2"] = True

        if char == PINS.get("key3") or char == "3":
            log.info("EMULATE BUTTON KEY3 PRESSED")
            BUTTON_KEY3.pin.drive_low()
            BUTTON_KEY3.pin.drive_high()
            cfg.BUTTONS_PRESSED["BUTTON_KEY3"] = True


# this must run before gpiozero button objects are created in order for button emulation to work.

if cfg.CONFIG.get("GENERAL").get("emulate"):
    Device.pin_factory = MockFactory()
    log = logging.getLogger(inspect.stack()[0][3])
    log.info("UP = 'w', DOWN = 'x', LEFT = 'a', RIGHT = 'd', CENTER = 's'")
    log.info("Press 'k' to break out of button tests.")
    cfg.BUTTON_EMULATION_THREAD = threading.Thread(
        name="button_emulator", target=button_emulation
    )
    cfg.BUTTON_EMULATION_THREAD.start()


def _println(pressed, gpio_pin):
    if cfg.BUTTON_TEST_IN_PROGRESS:
        if "LEFT" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_LEFT"]:
                cfg.BUTTONS_PRINTED["BUTTON_LEFT"] = True
                # https://fontawesome.com/v5.15/icons/chevron-left?style=solid
                print_term_icon_and_message("\uf053", f"{pressed}/{gpio_pin} PRESS")
                return
        if "RIGHT" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_RIGHT"]:
                cfg.BUTTONS_PRINTED["BUTTON_RIGHT"] = True
                # https://fontawesome.com/v5.15/icons/chevron-right?style=solid
                print_term_icon_and_message("\uf054", f"{pressed}/{gpio_pin} PRESS")
                return
        if "UP" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_UP"]:
                cfg.BUTTONS_PRINTED["BUTTON_UP"] = True
                # https://fontawesome.com/v5.15/icons/chevron-up?style=solid
                print_term_icon_and_message("\uf077", f"{pressed}/{gpio_pin} PRESS")
                return
        if "DOWN" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_DOWN"]:
                cfg.BUTTONS_PRINTED["BUTTON_DOWN"] = True
                # https://fontawesome.com/v5.15/icons/chevron-down?style=solid
                print_term_icon_and_message("\uf078", f"{pressed}/{gpio_pin} PRESS")
                return
        if "CENTER" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_CENTER"]:
                cfg.BUTTONS_PRINTED["BUTTON_CENTER"] = True
                # https://fontawesome.com/v5.15/icons/dot-circle?style=regular
                print_term_icon_and_message(
                    "\uf192", f"{pressed}/{gpio_pin} PRESS", icon_font=cfg.FAREGULAR
                )
                return
        if "KEY1" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_KEY1"]:
                cfg.BUTTONS_PRINTED["BUTTON_KEY1"] = True
                # https://fontawesome.com/v5.15/icons/dot-circle?style=regular
                print_term_icon_and_message(
                    "\uf11c", f"{pressed}/{gpio_pin} PRESS", icon_font=cfg.FAREGULAR
                )
                return
        if "KEY2" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_KEY2"]:
                cfg.BUTTONS_PRINTED["BUTTON_KEY2"] = True
                # https://fontawesome.com/v5.15/icons/dot-circle?style=regular
                print_term_icon_and_message(
                    "\uf11c", f"{pressed}/{gpio_pin} PRESS", icon_font=cfg.FAREGULAR
                )
                return
        if "KEY3" in pressed:
            if not cfg.BUTTONS_PRINTED["BUTTON_KEY3"]:
                cfg.BUTTONS_PRINTED["BUTTON_KEY3"] = True
                # https://fontawesome.com/v5.15/icons/dot-circle?style=regular
                print_term_icon_and_message(
                    "\uf11c", f"{pressed}/{gpio_pin} PRESS", icon_font=cfg.FAREGULAR
                )
                return


def button_press(gpio_pin: int):
    log = logging.getLogger(inspect.stack()[0][3])

    pressed = ""
    log.debug("TARGET PINS: %s" % PINS.items())
    log.debug("ACTIVE PIN: %s" % gpio_pin)
    for button, pin in PINS.items():
        if gpio_pin == pin:
            pressed = button.upper()
            break

    log.info(f"DETECTED PRESS ON GPIO PIN {gpio_pin} ({pressed})")

    # if we're doing the color test
    if cfg.COLOR_TEST_IN_PROGRESS:
        cfg.PRESSED = True

    # if we're doing the live interactive button test
    # print to OLED virtual terminal
    if cfg.BUTTON_TEST_IN_PROGRESS:
        if cfg.CONFIG.get("GENERAL").get("oled"):
            if pressed:
                if pressed in (
                    "LEFT",
                    "UP",
                    "DOWN",
                    "CENTER",
                    "RIGHT",
                    "KEY1",
                    "KEY2",
                    "KEY3",
                ):
                    # log.info(f"* {pressed} {gpio_pin}")
                    _println(pressed, gpio_pin)
                    return
                else:
                    cfg.TERMINAL.println(f"* GPIO PIN {gpio_pin} PRESSED")


def down_press():
    button_press(PINS["down"])
    cfg.BUTTONS_PRESSED["BUTTON_DOWN"] = True


def up_press():
    button_press(PINS["up"])
    cfg.BUTTONS_PRESSED["BUTTON_UP"] = True


def left_press():
    button_press(PINS["left"])
    cfg.BUTTONS_PRESSED["BUTTON_LEFT"] = True


def right_press():
    button_press(PINS["right"])
    cfg.BUTTONS_PRESSED["BUTTON_RIGHT"] = True


def center_press():
    button_press(PINS["center"])
    cfg.BUTTONS_PRESSED["BUTTON_CENTER"] = True


def key1_press():
    button_press(PINS["key1"])
    cfg.BUTTONS_PRESSED["BUTTON_KEY1"] = True


def key2_press():
    button_press(PINS["key2"])
    cfg.BUTTONS_PRESSED["BUTTON_KEY2"] = True


def key3_press():
    button_press(PINS["key2"])
    cfg.BUTTONS_PRESSED["BUTTON_KEY3"] = True


BUTTON_DOWN = None
BUTTON_UP = None
BUTTON_LEFT = None
BUTTON_RIGHT = None
BUTTON_CENTER = None
BUTTON_KEY1 = None
BUTTON_KEY2 = None
BUTTON_KEY3 = None


def init():
    global BUTTON_DOWN
    global BUTTON_UP
    global BUTTON_LEFT
    global BUTTON_RIGHT
    global BUTTON_CENTER

    BUTTON_DOWN = GPIO_Button(PINS["down"])
    BUTTON_UP = GPIO_Button(PINS["up"])
    BUTTON_LEFT = GPIO_Button(PINS["left"])
    BUTTON_RIGHT = GPIO_Button(PINS["right"])
    BUTTON_CENTER = GPIO_Button(PINS["center"])

    BUTTON_DOWN.when_pressed = down_press
    BUTTON_UP.when_pressed = up_press
    BUTTON_LEFT.when_pressed = left_press
    BUTTON_RIGHT.when_pressed = right_press
    BUTTON_CENTER.when_pressed = center_press

    if cfg.PLATFORM_M4 or cfg.PLATFORM_R4:
        BUTTON_KEY1 = GPIO_Button(PINS["key1"])
        BUTTON_KEY2 = GPIO_Button(PINS["key2"])
        BUTTON_KEY3 = GPIO_Button(PINS["key3"])
        BUTTON_KEY1.when_pressed = key1_press
        BUTTON_KEY2.when_pressed = key2_press
        BUTTON_KEY3.when_pressed = key3_press
