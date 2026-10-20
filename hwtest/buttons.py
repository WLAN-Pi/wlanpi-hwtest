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
import sys
import termios
import threading
import tty
from datetime import timedelta

import gpiod
from gpiod.line import Bias, Edge

import hwtest.cfg as cfg
from hwtest.oled import print_term_icon_and_message
from hwtest.platform import PLATFORM_R4

# Pi 3/4 and CM4 expose the header GPIOs on gpiochip0.
GPIO_CHIP = "/dev/gpiochip0"

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
    keys = {
        "w": "up",
        "x": "down",
        "a": "left",
        "d": "right",
        "s": "center",
        "1": "key1",
        "2": "key2",
        "3": "key3",
    }
    while cfg.RUNNING:
        char = getch().lower()
        log.debug(f"getch() detected {char}")

        if char == "k":
            log.info(
                "Button emulation stop requested ... Killing button emulation ... Press CTRL-C to exit ..."
            )
            break

        name = keys.get(char)
        if name in PINS:
            log.info(f"EMULATE BUTTON {name.upper()} PRESS")
            PRESS_HANDLERS[name]()


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
    button_press(PINS["key3"])
    cfg.BUTTONS_PRESSED["BUTTON_KEY3"] = True


PRESS_HANDLERS = {
    "up": up_press,
    "down": down_press,
    "left": left_press,
    "right": right_press,
    "center": center_press,
    "key1": key1_press,
    "key2": key2_press,
    "key3": key3_press,
}


def monitor_buttons(request):
    handlers = {pin: PRESS_HANDLERS[name] for name, pin in PINS.items()}
    with request:
        while cfg.RUNNING:
            if request.wait_edge_events(timedelta(seconds=1)):
                for event in request.read_edge_events():
                    handler = handlers.get(event.line_offset)
                    if handler:
                        handler()


def init():
    log = logging.getLogger(inspect.stack()[0][3])

    if cfg.CONFIG.get("GENERAL").get("emulate"):
        log.info("UP = 'w', DOWN = 'x', LEFT = 'a', RIGHT = 'd', CENTER = 's'")
        log.info("Press 'k' to break out of button tests.")
        threading.Thread(
            name="button_emulator", target=button_emulation, daemon=True
        ).start()
        return

    settings = gpiod.LineSettings(
        bias=Bias.PULL_UP,
        edge_detection=Edge.FALLING,
        debounce_period=timedelta(microseconds=10),
    )
    request = gpiod.request_lines(
        GPIO_CHIP,
        consumer="hwtest",
        config=dict.fromkeys(PINS.values(), settings),
    )
    threading.Thread(
        name="button_monitor", target=monitor_buttons, args=(request,), daemon=True
    ).start()
