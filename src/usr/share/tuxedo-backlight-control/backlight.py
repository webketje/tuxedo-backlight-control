#!/usr/bin/pkexec /usr/bin/python3

import os
from sys import argv
from colors import colors
from backlight_control import *
import subprocess

sd = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    if len(argv) == 1:
        exit('Tuxedo Backlight Ctrl: No command specified. Try "backlight --help" to list available commands')

    cmd = argv[1]
    if cmd == '--help' or cmd == '-h':
        with open(sd + '/help.txt', 'r') as fin:
            exit(fin.read())

    if cmd == '--version' or cmd == '-v':
        exit(BacklightControl.VERSION)
            
    if not os.path.isdir(BacklightControl.DEVICE_PATH):
        exit('Tuxedo Backlight Ctrl: The tuxedo_keyboard module is not installed at ' + BacklightControl.DEVICE_PATH)

    if cmd == 'ui':
        subprocess.call(['/usr/share/tuxedo-backlight-control/ui.py'])
    elif cmd == 'off':
        backlight.state = 0
    elif len(argv) == 2 and cmd in backlight.modes:
        backlight.state = 1
        backlight.mode = cmd
    elif len(argv) == 3 and cmd == 'color' and argv[2] in list(BacklightControl.colors.keys()):
        backlight.state = 1
        backlight.set_single_color(argv[2])
    elif len(argv) == 6:
        backlight.state = 1
        for index, region in enumerate(backlight.regions):
            setattr(backlight, 'color_' + region, argv[2 + index])
