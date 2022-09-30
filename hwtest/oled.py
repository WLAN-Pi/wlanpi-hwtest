# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

"""
wlanpi-hwtest.oled
~~~~~~~~~~~~~~~~~~

define and init OLED objects for hwtest
"""

import inspect
import logging
import os
import sys
import threading
import time

import luma.core
from luma.core import cmdline, error

import hwtest.cfg as cfg
from hwtest.__version__ import __version__
from hwtest.platform import (PLATFORM_M4, PLATFORM_PRO, PLATFORM_R4,
                             PLATFORM_UNKNOWN)

# set possible vars to None
DISPLAY_TYPE = None
I2C_PORT = None
I2C_ADDRESS = None
SPI_PORT = None
SPI_DEVICE = None
INTERFACE_TYPE = None
WIDTH = None
HEIGHT = None
GPIO_DATA_COMMAND = None
H_OFFSET = None
V_OFFSET = None

COLOR_ORDER_BGR = None
BACKLIGHT_ACTIVE = None
GPIO_RESET = None
GPIO_BACKLIGHT = None
BACKLIGHT_ACTIVE = None

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


def get_actual_args():
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

    if GPIO_RESET:
        actual_args.append("--gpio-reset")
        actual_args.append(GPIO_RESET)

    if GPIO_BACKLIGHT:
        actual_args.append("--gpio-backlight")
        actual_args.append(GPIO_BACKLIGHT)

    if BACKLIGHT_ACTIVE:
        actual_args.append("--backlight-active")
        actual_args.append(BACKLIGHT_ACTIVE)

    if COLOR_ORDER_BGR:
        actual_args.append("--bgr")
    return actual_args


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """

    log = logging.getLogger(inspect.stack()[0][3])
    log.debug("starting get_device() with actual_args: %s" % actual_args)
    if actual_args is None:
        actual_args = sys.argv[1:]

    luma_parser = cmdline.create_parser(description="luma.examples arguments")
    args = luma_parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        log.debug(f"{config}")
        args = luma_parser.parse_args(config + actual_args)
    log.debug(f"{args}")

    # create device
    try:
        device = cmdline.create_device(args)
        log.debug(display_settings(device, args))
        return device

    except error.Error as _error:
        luma_parser.error(_error)
        log.exception("Luma parser error ... exiting ...", exc_info=True)
        sys.exit(-1)


def print_message_colors(message, fgcolor, bgcolor):
    if cfg.CONFIG.get("GENERAL").get("oled"):
        cfg.TERMINAL._fgcolor = fgcolor
        cfg.TERMINAL.default_fgcolor = fgcolor
        cfg.TERMINAL.default_bgcolor = bgcolor
        cfg.TERMINAL._bgcolor = bgcolor
        cfg.TERMINAL.println(message)


def oled_print_task(animate, icon, icon_font, font, message):
    cfg.TERMINAL.animate = animate
    cfg.TERMINAL.font = icon_font
    cfg.TERMINAL.puts(f"{icon}")
    cfg.TERMINAL.font = font
    cfg.TERMINAL.puts(f" {message}\n")
    cfg.TERMINAL.flush()
    if not animate:
        cfg.TERMINAL.animate = True


OUT = []

OLED_PRINTER_TASK_STARTED = False


def oled_print_task_thread():
    while cfg.RUNNING:
        if len(OUT) > 0:
            oled_print_task(*OUT.pop(0))
        time.sleep(0.01)


def print_term_icon_and_message(
    icon, message, icon_font=cfg.FASOLID, font=cfg.FIRACODE, animate=False
):
    global OLED_PRINTER_TASK_STARTED
    if cfg.CONFIG.get("GENERAL").get("oled"):
        if not OLED_PRINTER_TASK_STARTED:
            OLED_PRINTER_TASK_STARTED = True
            t = threading.Thread(target=oled_print_task_thread)
            t.start()
        OUT.append(
            (
                animate,
                icon,
                icon_font,
                font,
                message,
            )
        )


def init_oled_luma_terminal():
    """initialize terminal test"""
    log = logging.getLogger(inspect.stack()[0][3])
    global DISPLAY_TYPE
    global GPIO_DATA_COMMAND
    global GPIO_RESET
    global GPIO_BACKLIGHT
    global BACKLIGHT_ACTIVE
    global H_OFFSET
    global V_OFFSET
    global INTERFACE_TYPE
    global SPI_PORT
    global SPI_DEVICE
    global WIDTH
    global HEIGHT
    log.debug("cfg.PLATFORM is %s" % cfg.PLATFORM)
    if cfg.PLATFORM == PLATFORM_R4:
        # st7735 128 x 128 settings for "R4/M4 1.44 in LCD Display HAT"
        DISPLAY_TYPE = "st7735"
        GPIO_DATA_COMMAND = "25"
        GPIO_RESET = "27"
        GPIO_BACKLIGHT = "24"
        H_OFFSET = "1"
        V_OFFSET = "2"
        BACKLIGHT_ACTIVE = "high"
    else:
        # ssd1351 128 x 128 settings for "WLAN Pi "Pro Rev2"
        DISPLAY_TYPE = "ssd1351"
    log.debug("DISPLAY_TYPE %s" % DISPLAY_TYPE)

    COLOR_ORDER_BGR = True
    INTERFACE_TYPE = "spi"
    SPI_PORT = 0
    SPI_DEVICE = 0
    WIDTH = "128"
    HEIGHT = "128"

    from luma.core.virtual import terminal

    actual_args = get_actual_args()
    device = get_device(actual_args=actual_args)

    if cfg.PLATFORM == PLATFORM_PRO:
        device.contrast(128)

    cfg.TERMINAL = terminal(
        device,
        cfg.FIRACODE,
        color="white",
        bgcolor="black",
        line_height=15,
        animate=False,
    )
    cfg.TERMINAL.println(f"WLANPI HWTEST")
    cfg.TERMINAL.println(f"VERSION: {__version__}")
    cfg.TERMINAL.println(f"PLATFORM: {cfg.PLATFORM}")
