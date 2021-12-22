# -*- coding: utf-8 -*-

import time

from gpiozero import Button

buttons = {}

for id in range(2, 28):
    buttons[str(id)] = Button(id)

running = True

while running:
    for number, button in buttons.items():
        if button.is_pressed:
            print(f"Button {str(number)} was pressed")

    time.sleep(0.1)

# TODO refactor into button test. do not continue until buttons we care about have been registered.
