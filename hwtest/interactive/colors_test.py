# -*- coding: utf-8 -*-
#
# wlanpi-hwtest : verification tools for the WLAN Pi Pro
# Copyright : (c) 2022 Josh Schmelzle
# License : BSD-3-Clause


import hwtest.cfg as cfg
import hwtest.oled as oled


def button_pressed() -> bool:
    return cfg.PRESSED


def test_colors():
    cfg.COLOR_TEST_IN_PROGRESS = True

    for color in ["red", "green", "blue", "white"]:
        for _n in range(1, 9):
            oled.print_message_colors("", "black", color)

        oled.print_message_colors("PRESS ANY BUTTON TO CONTINUE", "black", color)
        try:
            while cfg.RUNNING:
                if button_pressed():
                    cfg.PRESSED = False
                    break
        except KeyboardInterrupt:
            pass

    oled.print_message_colors("", "white", "black")
    oled.print_message_colors("", "white", "black")
    oled.print_message_colors("", "white", "black")

    cfg.COLOR_TEST_IN_PROGRESS = False

    assert True
