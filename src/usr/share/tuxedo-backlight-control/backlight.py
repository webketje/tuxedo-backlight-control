#!/usr/bin/pkexec /usr/bin/python3

import os
import subprocess
from sys import argv

from backlight_control import BacklightControl, backlight

sd = os.path.dirname(os.path.realpath(__file__))


def error_invalid_brightness(arg: str):
    return f"Error: Invalid argument '{arg}' provided. Please provide a number from 0 - 255 to set brightness"

def error_missing_cmd():
    return "Error: No command specified. Try 'backlight --help' to list available commands."

def error_missing_arg(cmd: str):
    return f"Error: No argument specified for '{cmd}'. Try 'backlight --help' to list available comamnds and valid arguments."

def error_no_driver():
    return f"Error: The tuxedo_keyboard module is not installed at {BacklightControl.DEVICE_PATH}"


if __name__ == "__main__":
    if len(argv) == 1:
        exit(error_missing_cmd())

    cmd = argv[1]
    if cmd == "--help" or cmd == "-h":
        with open(sd + "/help.txt", "r") as fin:
            exit(fin.read())

    if cmd == "--version" or cmd == "-v":
        exit(BacklightControl.VERSION)

    if not os.path.isdir(BacklightControl.DEVICE_PATH):
        exit(error_no_driver())

    colorlist = list(BacklightControl.colors.keys())

    if cmd == "ui":
        from ui import init
        init()
        exit()

    if cmd == "off":
        backlight.state = 0
        exit()

    if len(argv) == 2 and cmd in backlight.modes:
        backlight.state = 1
        backlight.mode = cmd

    if len(argv) < 3:
        exit(error_missing_arg(cmd))

    arg = argv[2]
    if cmd == "brightness":
        backlight.state = 1
        try:
            arg = int(arg)
        except ValueError as error:
            exit(error_invalid_brightness(arg))
        if arg > 255 or arg < 0:
            exit(error_invalid_brightness(arg))

        backlight.brightness = arg
    elif len(argv) == 3 and cmd == "color" and arg in colorlist:
        backlight.state = 1
        backlight.set_single_color(arg)
    elif len(argv) == 6:
        backlight.state = 1
        for index, region in enumerate(backlight.regions):
            setattr(backlight, "color_" + region, argv[2 + index])
