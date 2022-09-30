# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for WLAN Pi
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause

"""
wlanpi-hwtest:platform
~~~~~~~~~~~~~~~~~~~~~~

platform types and models
"""

import subprocess

PLATFORM_UNKNOWN = "Unknown"
PLATFORM_PRO = "Pro"
PLATFORM_R4 = "R4"
PLATFORM_M4 = "M4"

CPUINFO = subprocess.check_output("cat /proc/cpuinfo", shell=True).decode().strip()

PLATFORM = PLATFORM_UNKNOWN

if "Raspberry Pi 3 Model B Rev 1.2" in CPUINFO:
    PLATFORM = PLATFORM_R4

if "Raspberry Pi 4 Model B" in CPUINFO:
    PLATFORM = PLATFORM_R4

if "Compute Module 4" in CPUINFO:
    PLATFORM = PLATFORM_PRO

LSPCI_INFO subprocess.check_output("lspci", shell=True).decode().strip()

if "VL805" not in LSPCI_INFO
    PLATFORM = PLATFORM_M4