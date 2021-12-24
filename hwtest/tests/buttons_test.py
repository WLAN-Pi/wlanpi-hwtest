# -*- coding: utf-8 -*-


import inspect
import logging
import signal
import sys
import termios
import threading
import tty

import pytest
from gpiozero import Button as GPIO_Button
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

from hwtest.oled import BUTTONS_PINS
from hwtest.testing import EMULATE, RUNNING, TERMINAL, TESTING_IN_PROGRESS


@pytest.fixture(scope="session", autouse=True)
def term_handler():
    orig = signal.signal(signal.SIGTERM, signal.getsignal(signal.SIGINT))
    yield
    signal.signal(signal.SIGTERM, orig)


# this must run before gpiozero button objects are created in order for button emulation to work.
if EMULATE:
    Device.pin_factory = MockFactory()

BUTTONS = {}

PINS = BUTTONS_PINS

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

BUTTON_DOWN = GPIO_Button(PINS["down"])
BUTTON_UP = GPIO_Button(PINS["up"])
BUTTON_LEFT = GPIO_Button(PINS["left"])
BUTTON_RIGHT = GPIO_Button(PINS["right"])
BUTTON_CENTER = GPIO_Button(PINS["center"])


def button_press(gpio_pin: int):
    log = logging.getLogger(inspect.stack()[0][3])

    pressed = ""
    for button, pin in PINS.items():
        if gpio_pin == pin:
            pressed = button.upper()
    log.info(f"DETECTED PRESS ON GPIO PIN {gpio_pin}")

    def _println():
        TERMINAL.println(f"* {pressed} ({gpio_pin}) DETECTED")

    if TESTING_IN_PROGRESS:
        if pressed:
            if pressed == "LEFT":
                if not BUTTONS_PRINTED["BUTTON_LEFT"]:
                    BUTTONS_PRINTED["BUTTON_LEFT"] = True
                    _println()
                    return
            if pressed == "UP":
                if not BUTTONS_PRINTED["BUTTON_UP"]:
                    BUTTONS_PRINTED["BUTTON_UP"] = True
                    _println()
                    return
            if pressed == "DOWN":
                if not BUTTONS_PRINTED["BUTTON_DOWN"]:
                    BUTTONS_PRINTED["BUTTON_DOWN"] = True
                    _println()
                    return
            if pressed == "CENTER":
                if not BUTTONS_PRINTED["BUTTON_CENTER"]:
                    BUTTONS_PRINTED["BUTTON_CENTER"] = True
                    _println()
                    return
            if pressed == "RIGHT":
                if not BUTTONS_PRINTED["BUTTON_RIGHT"]:
                    BUTTONS_PRINTED["BUTTON_RIGHT"] = True
                    _println()
                    return
        else:
            TERMINAL.println(f"* GPIO PIN {gpio_pin} PRESSED")


def down():
    button_press(PINS["down"])
    BUTTONS_PRESSED["BUTTON_DOWN"] = True


def up():
    button_press(PINS["up"])
    BUTTONS_PRESSED["BUTTON_UP"] = True


def left():
    button_press(PINS["left"])
    BUTTONS_PRESSED["BUTTON_LEFT"] = True


def right():
    button_press(PINS["right"])
    BUTTONS_PRESSED["BUTTON_RIGHT"] = True


def center():
    button_press(PINS["center"])
    BUTTONS_PRESSED["BUTTON_CENTER"] = True


BUTTON_DOWN.when_pressed = down
BUTTON_UP.when_pressed = up
BUTTON_LEFT.when_pressed = left
BUTTON_RIGHT.when_pressed = right
BUTTON_CENTER.when_pressed = center


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def all_expected_buttons_pressed() -> bool:
    global BUTTONS_PRESSED
    return all(value == True for value in BUTTONS_PRESSED.values())


def button_emulation():
    log = logging.getLogger(inspect.stack()[0][3])
    while not all_expected_buttons_pressed():
        char = getch()

        if char == "k" or char == "K":
            log.info("Stop requested ... Breaking out of button emulation ...")
            break

        if char == "8" or char == "w":
            log.info("EMULATE UP PRESS")
            BUTTON_UP.pin.drive_low()
            BUTTON_UP.pin.drive_high()
            BUTTONS_PRESSED["BUTTON_UP"] = True

        if char == "2" or char == "x":
            log.info("EMULATE DOWN PRESS")
            BUTTON_DOWN.pin.drive_low()
            BUTTON_DOWN.pin.drive_high()
            BUTTONS_PRESSED["BUTTON_DOWN"] = True

        if char == "4" or char == "a":
            log.info("BUTTON_LEFT PRESSED")
            BUTTON_LEFT.pin.drive_low()
            BUTTON_LEFT.pin.drive_high()
            BUTTONS_PRESSED["BUTTON_LEFT"] = True

        if char == "6" or char == "d":
            log.info("BUTTON_RIGHT PRESSED")
            BUTTON_RIGHT.pin.drive_low()
            BUTTON_RIGHT.pin.drive_high()
            BUTTONS_PRESSED["BUTTON_RIGHT"] = True

        if char == "5" or char == "s":
            log.info("BUTTON_CENTER PRESSED")
            BUTTON_CENTER.pin.drive_low()
            BUTTON_CENTER.pin.drive_high()
            BUTTONS_PRESSED["BUTTON_CENTER"] = True


def test_5x_buttons():
    log = logging.getLogger(inspect.stack()[0][3])
    log.info("test_buttons()")
    TERMINAL.println("PRESS ALL BUTTONS")
    TERMINAL.println("   TO CONTINUE")

    if EMULATE:
        log.info("UP = 'w', DOWN = 'x', LEFT = 'a', RIGHT = 'd', CENTER = 's'")
        log.info("Press 'k' to break out of button tests.")
        e = threading.Thread(name="button_emulator", target=button_emulation)
        e.start()
        # e.join()

    try:
        while RUNNING:
            if all_expected_buttons_pressed():
                log.info("ALL BUTTONS HAVE BEEN PRESSED")
                break
    except KeyboardInterrupt:
        pass

    global TESTING_IN_PROGRESS
    TESTING_IN_PROGRESS = False

    assert all_expected_buttons_pressed() == True
