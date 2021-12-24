# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.oled
~~~~~~~~~~~~~~~~~~

oled stuff
"""

import inspect
import logging
import os
import sys

import luma.core
from luma.core import cmdline, error

# set possible vars to None
DISPLAY_TYPE = None
I2C_PORT = None
I2C_ADDRESS = None
SPI_PORT = None
SPI_DEVICE = None
INTERFACE_TYPE = None
WIDTH = None
HEIGHT = None
COLOR_ORDER_BGR = False
GPIO_DATA_COMMAND = None
H_OFFSET = None
V_OFFSET = None

# Button mapping (WLANPi Pro)
BUTTONS_WLANPI_PRO = {
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
}

BUTTONS_PINS = {}

if os.path.exists("/boot/waveshare"):
    # st7735 128 x 128
    DISPLAY_TYPE = "st7735"
    GPIO_DATA_COMMAND = "25"
    H_OFFSET = "1"
    V_OFFSET = "2"
    BUTTONS_PINS = BUTTONS_WAVESHARE
else:
    # ssd1351 128 x 128
    DISPLAY_TYPE = "ssd1351"
    BUTTONS_PINS = BUTTONS_WLANPI_PRO

INTERFACE_TYPE = "spi"
SPI_PORT = 0
SPI_DEVICE = 0
WIDTH = "128"
HEIGHT = "128"
COLOR_ORDER_BGR = True

HEIGHT_OFFSET = 64
DISPLAY_MODE = "RGB"

PAGE_SLEEP = 300  # Time in secs before sleep
PAGE_WIDTH = 128  # Pixel size of screen width
PAGE_HEIGHT = 64 + HEIGHT_OFFSET  # Pixel size of screen height
NAV_BAR_TOP = 54 + HEIGHT_OFFSET  # Top pixel number of nav bar
STATUS_BAR_HEIGHT = 16
SYSTEM_BAR_HEIGHT = 15

# ignore PIL debug messages
logging.getLogger("PIL").setLevel(logging.ERROR)


def display_settings(device, args) -> str:
    """
    Display a short summary of the settings.
    """
    iface = ""
    display_types = cmdline.get_display_types()
    if args.display not in display_types["emulator"]:
        iface = "Interface: {}\n".format(args.interface)

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = "unknown"

    version = "luma.{} {} (luma.core {})".format(
        lib_name, lib_version, luma.core.__version__
    )

    return "{0}\nVersion: {1}\nDisplay: {2}\n{3}Dimensions: {4} x {5}\nMode: {6}\n{7}".format(
        "-" * 50,
        version,
        args.display,
        iface,
        device.width,
        device.height,
        device.mode,
        "-" * 50,
    )


actual_args = []

if DISPLAY_TYPE:
    actual_args.append("-d")
    actual_args.append(DISPLAY_TYPE)

if INTERFACE_TYPE:
    actual_args.append("--interface")
    actual_args.append(INTERFACE_TYPE)


if INTERFACE_TYPE == "spi":
    actual_args.append("--spi-port")
    actual_args.append(SPI_PORT)
    actual_args.append("--spi-device")
    actual_args.append(SPI_DEVICE)

if WIDTH:
    actual_args.append("--width")
    actual_args.append(WIDTH)

if HEIGHT:
    actual_args.append("--height")
    actual_args.append(HEIGHT)

if GPIO_DATA_COMMAND:
    actual_args.append("--gpio-data-command")
    actual_args.append(GPIO_DATA_COMMAND)

if H_OFFSET:
    actual_args.append("--h-offset")
    actual_args.append(H_OFFSET)

if V_OFFSET:
    actual_args.append("--v-offset")
    actual_args.append(V_OFFSET)


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """

    log = logging.getLogger(inspect.stack()[0][3])

    if actual_args is None:
        actual_args = sys.argv[1:]
    luma_parser = cmdline.create_parser(description="luma.examples arguments")
    args = luma_parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = luma_parser.parse_args(config + actual_args)

    # create device
    try:
        device = cmdline.create_device(args)
        log.info(display_settings(device, args))
        return device

    except error.Error as _error:
        luma_parser.error(_error)
        log.exception("Luma parser error ... exiting ...", exc_info=True)
        sys.exit(-1)


device = get_device(actual_args=actual_args)

# Init function of the OLED
def init():
    device.contrast(128)


def clearDisplay():
    # blank = Image.new("RGBA", device.size, "black")
    # device.display(blank.convert(device.mode))
    device.clear()


def drawImage(image):
    device.display(image.convert(device.mode))
    # device.display(image)
