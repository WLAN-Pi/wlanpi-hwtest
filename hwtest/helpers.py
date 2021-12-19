# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2021 WLAN Pi Project
# License : MIT

"""
wlanpi-hwtest.helpers
~~~~~~~~~~~~~~~~~~~~~

provides functions which help setup the app.
"""

# standard library imports
import argparse
import logging
import logging.config
import shutil
import signal
import sys

# app imports
from .__version__ import __version__

__tools = ["lspci", "lsusb", "modprobe", "modinfo"]

# are the required tools installed?
for tool in __tools:
    if shutil.which(tool) is None:
        print(f"It looks like you do not have {tool} installed.")
        print("Please install using your distro's package manager.")
        sys.exit(signal.SIGABRT)


def setup_logger(args) -> None:
    """Configure and set logging levels"""
    logging_level = logging.INFO

    if args.debug:
        logging_level = logging.DEBUG

    default_logging = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "default": {
                "level": logging_level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {"": {"handlers": ["default"], "level": logging_level}},
    }
    logging.config.dictConfig(default_logging)


def setup_parser() -> argparse.ArgumentParser:
    """Set default values and handle arg parser"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="wlanpi-hwtest is a verification tool for the WLAN Pi Pro",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="enable debug logging output",
    )
    parser.add_argument("--version", "-V", action="version", version=f"{__version__}")
    return parser
