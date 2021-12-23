# -*- coding: utf-8 -*-


import inspect
import logging
import sys
import termios
import threading
import tty

from gpiozero import Button as GPIO_Button
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

from hwtest.testing import TERMINAL

BUTTONS = {}

PINS = {
    "up": 22,
    "down": 5,
    "left": 17,
    "right": 27,
    "center": 6,
}


def button_press(gpio_pin: int):
    global TERMINAL
    pressed = ""
    for button, pin in PINS.items():
        if gpio_pin == pin:
            pressed = button
    TERMINAL.println(f" - {pressed.upper() if pressed else gpio_pin} PRESSED")


def down():
    global PINS
    button_press(PINS["down"])


def up():
    global PINS
    button_press(PINS["up"])


def left():
    global PINS
    button_press(PINS["left"])


def right():
    global PINS
    button_press(PINS["right"])


def center():
    global PINS
    button_press(PINS["center"])


# This is required for button emulation before the gpiozero button objects are created
Device.pin_factory = MockFactory()

BUTTON_DOWN = GPIO_Button(PINS["down"])
BUTTON_UP = GPIO_Button(PINS["up"])
BUTTON_LEFT = GPIO_Button(PINS["left"])
BUTTON_RIGHT = GPIO_Button(PINS["right"])
BUTTON_CENTER = GPIO_Button(PINS["center"])

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


LISTOFBUTTONS = {
    "BUTTON_UP": False,
    "BUTTON_DOWN": False,
    "BUTTON_LEFT": False,
    "BUTTON_RIGHT": False,
    "BUTTON_CENTER": False,
}


def emulate_buttons():
    log = logging.getLogger(inspect.stack()[0][3])
    global LISTOFBUTTONS
    while not all(value == True for value in LISTOFBUTTONS.values()):
        char = getch()

        if char == "k" or char == "K":
            log.info("Stop requested ... Breaking out of emulate buttons ...")
            break

        if char == "8" or char == "w":
            log.info("BUTTON_UP PRESSED")
            LISTOFBUTTONS["BUTTON_UP"] = True
            BUTTON_UP.pin.drive_low()
            BUTTON_UP.pin.drive_high()

        if char == "2" or char == "x":
            log.info("BUTTON_DOWN PRESSED")
            LISTOFBUTTONS["BUTTON_DOWN"] = True
            BUTTON_DOWN.pin.drive_low()
            BUTTON_DOWN.pin.drive_high()

        if char == "4" or char == "a":
            log.info("BUTTON_LEFT PRESSED")
            LISTOFBUTTONS["BUTTON_LEFT"] = True
            BUTTON_LEFT.pin.drive_low()
            BUTTON_LEFT.pin.drive_high()

        if char == "6" or char == "d":
            log.info("BUTTON_RIGHT PRESSED")
            LISTOFBUTTONS["BUTTON_RIGHT"] = True
            BUTTON_RIGHT.pin.drive_low()
            BUTTON_RIGHT.pin.drive_high()

        if char == "5" or char == "s":
            log.info("BUTTON_CENTER PRESSED")
            LISTOFBUTTONS["BUTTON_CENTER"] = True
            BUTTON_CENTER.pin.drive_low()
            BUTTON_CENTER.pin.drive_high()

    log.info("ALL BUTTONS HAVE BEEN PRESSED")


def test_buttons():
    log = logging.getLogger(inspect.stack()[0][3])
    log.info("UP = 'w', DOWN = 'x', LEFT = 'a', RIGHT = 'd', CENTER = 's'")
    log.info("Press 'k' to break out of button tests.")
    e = threading.Thread(name="button-emulator", target=emulate_buttons)
    e.start()
    TERMINAL.println("PRESS ALL BUTTONS")
    TERMINAL.println("TO CONTINUE")
    e.join()
    assert all(value == True for value in LISTOFBUTTONS.values()) == True
