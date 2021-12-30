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

import argparse
import configparser
import inspect
import logging
import logging.config
import os
import shutil
import signal
import sys
from distutils.util import strtobool
from typing import Any, Dict

import hwtest.cfg as cfg

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


def get_config_file() -> str:
    conf = "/etc/wlanpi-hwtest/config.ini"

    if not os.path.isfile(conf):
        dev_conf = os.path.join(cfg.HERE, "../install/etc/wlanpi-hwtest/config.ini")
        if os.path.isfile(dev_conf):
            conf = dev_conf
    return conf


def setup_parser() -> argparse.ArgumentParser:
    """Set default values and handle arg parser"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="wlanpi-hwtest is an VLI USB Controller EEPROM updater and hardware testing tool for the WLAN Pi Pro.",
    )
    parser.add_argument(
        "--config",
        type=str,
        metavar="FILE",
        default=get_config_file(),
        help=argparse.SUPPRESS,
        # help="specify path for configuration file (default: /etc/wlanpi-hwtest/config.ini)",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="enable debug logging output",
    )
    parser.add_argument(
        "-e",
        "--emulate",
        dest="emulate",
        action="store_true",
        default=False,
        help="enable keyboard emulation",
    )
    parser.add_argument(
        "--oled",
        dest="oled",
        action="store_true",
        default=None,
        help="enable OLED and interactive (I/A) tests",
    )
    parser.add_argument(
        "--firmware",
        dest="firmware",
        action="store_true",
        default=None,
        help="enable VL805 firmware check",
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="enable verbose printing of results to oled",
    )
    parser.add_argument("--version", "-V", action="version", version=f"{__version__}")
    return parser


def ConfigParser_to_Dict(config: configparser.ConfigParser) -> Dict:
    """
    Convert ConfigParser object to dictionary.
    The resulting dictionary has sections as keys which point to a dict of the
    section options as key => value pairs.
    If there is a string representation of truth, it is converted from str to bool.
    """
    _dict: "Dict[str, Any]" = {}
    for section in config.sections():
        _dict[section] = {}
        for key, _value in config.items(section):
            try:
                _value = bool(strtobool(_value))  # type: ignore
            except ValueError:
                pass
            _dict[section][key] = _value
    return _dict


def read_config(args) -> Dict:
    """Create the configuration (SSID, channel, interface, etc) for the Profiler"""
    log = logging.getLogger(inspect.stack()[0][3])

    # load in config (a: from default location "/etc/wlanpi-hwtest/config.ini" or b: from provided)
    if os.path.isfile(args.config):
        cp = configparser.ConfigParser()
        cp.read(args.config)

        # we want to work with a dict whether we have config.ini or not
        config = ConfigParser_to_Dict(cp)
    else:
        log.warning("can not find config at %s", args.config)
        config = {}

    if "GENERAL" not in config:
        config["GENERAL"] = {}

    if "oled" not in config["GENERAL"]:
        config["GENERAL"]["oled"] = True

    # handle args
    #  - args passed in take precedent over config.ini values
    #  - did user pass in options that over-ride defaults?
    if args.oled:
        config["GENERAL"]["oled"] = args.oled

    if args.firmware:
        config["GENERAL"]["firmware"] = args.firmware

    if args.verbose:
        config["GENERAL"]["verbose"] = args.verbose
    else:
        config["GENERAL"]["verbose"] = False

    if args.emulate:
        config["GENERAL"]["emulate"] = args.emulate

    return config
