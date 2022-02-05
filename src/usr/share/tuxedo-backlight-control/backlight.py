#!/usr/bin/pkexec /usr/bin/python3

import os
import sys

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
    if len(sys.argv) == 1:
        sys.exit(error_missing_cmd())

    CMD = sys.argv[1]
    if CMD in ("--help", "-h"):
        with open(sd + "/help.txt", "r") as fin:
            sys.exit(fin.read())

    if CMD in ("--version", "-v"):
        sys.exit(BacklightControl.VERSION)

    if not os.path.isdir(BacklightControl.DEVICE_PATH):
        sys.exit(error_no_driver())

    COLOR_LIST = list(BacklightControl.colors.keys())

    if CMD == "ui":
        from ui import init
        init()
        sys.exit()

    if CMD == "off":
        backlight.state = 0
        sys.exit()

    if len(sys.argv) == 2 and CMD in backlight.modes:
        backlight.state = 1
        backlight.mode = CMD

    if len(sys.argv) < 3:
        sys.exit(error_missing_arg(CMD))

    ARG = sys.argv[2]
    if CMD == "brightness":
        backlight.state = 1
        try:
            ARG = int(ARG)
        except ValueError as error:
            sys.exit(error_invalid_brightness(ARG))
        if ARG > 255 or ARG < 0:
            sys.exit(error_invalid_brightness(ARG))

        backlight.brightness = str(ARG)
    elif len(sys.argv) == 3 and CMD == "color" and ARG in COLOR_LIST:
        backlight.state = 1
        backlight.set_single_color(ARG)
    elif len(sys.argv) == 6:
        backlight.state = 1
        for index, region in enumerate(backlight.regions):
            setattr(backlight, "color_" + region, sys.argv[2 + index])
