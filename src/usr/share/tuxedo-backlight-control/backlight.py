#!/usr/bin/pkexec /usr/bin/python3

import os
import subprocess
from sys import argv
import argparse
from backlight_control import BacklightControl, backlight

def exec_ui(args):
    from ui import init
    init()
    exit()

def set_color(args):
    if len(args.colors) == 1:
        BacklightControl.set_single_color(args.values[0])
    else:
        for region in BacklightControl.regions:
            index = BacklightControl.regions.index(region)
            if len(args.values) > index:
                mapped_color = BacklightControl.find_color_by_key(args.values[index])
                BacklightControl.set_device_param('color_' + region, mapped_color)

def set_mode(args):
    BacklightControl.mode = args.value
def set_off(args):
    BacklightControl.state = '0'
def set_brightness(args):
    BacklightControl.brightness = args.value

colorlist = BacklightControl.colors.keys()
parser = argparse.ArgumentParser(
    prog='backlight',
    description='<tuxedo-backlight-control> - v0.7 - 2020-08-14, by Kevin Van Lierde <kevin.van.lierde@gmail.com>',
    epilog="""Report bugs at https://github.com/webketje/tuxedo-backlight-control/issues.\n
For info on the tuxedo_keyboard kernel module, see https://github.com/tuxedocomputers/tuxedo-keyboard""")
subparsers = parser.add_subparsers()

colorparser = subparsers.add_parser('color',
    help="""
        Set the keyboard backlight to a single color.
        Alternatively, set the keyboard to 1-4 distinct colors, in the order: left, center, right, extra.
        Available colors are: {colors} .
        Only regions supported by your keyboard will have effect.
    """.format(colors=', '.join([str(x) for x in BacklightControl.colors.keys()]))
)
colorparser.add_argument('values', choices=colorlist, nargs='+')
colorparser.set_defaults(action=set_color)

modeparser = subparsers.add_parser('mode', help='Set the keyboard backlight to <mode>, one of: breathe, cycle, dance, flash, random, tempo, wave')
modeparser.add_argument('value', choices=BacklightControl.modes, nargs=1, help='Set the keyboard backlight to <mode>')
modeparser.set_defaults(action=set_mode)

brightness_args = subparsers.add_parser('brightness', help='Set keyboard backlight brightness from 0-255')
brightness_args.add_argument('value', type=int)
brightness_args.set_defaults(action=set_brightness)

stateparser = subparsers.add_parser('off', help='Turn off keyboard backlight')
stateparser.set_defaults(action=set_off)

uiparser = subparsers.add_parser('ui', help='Start the TUXEDO Backlight Control UI')
uiparser.set_defaults(action=exec_ui)

parser.add_argument('-v', '--version', action='version', version='0.7', help='Display app version')
parsed = parser.parse_args(argv[1:])

if 'action' in vars(parsed):
    parsed.action(parsed)