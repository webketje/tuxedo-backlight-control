#!/usr/bin/pkexec /usr/bin/python3

import os
import re

from colors import colors

if os.path.isfile('/etc/tuxedo-backlight-control/colors.conf'):
    colors_conf = open('/etc/tuxedo-backlight-control/colors.conf')
    for line in colors_conf:
        match = re.search('([\da-z_]+)=([\da-f]{6})', line)
        if match and len(match.groups()) == 2:
            colors[match.groups()[0]] = match.groups()[1]

class BacklightControl():
    """
    Abstraction on top of tuxedo_keyboard C driver interface for keyboard backlight
    """

    DEVICE_PATH = '/sys/devices/platform/tuxedo_keyboard/'
    MODULE_PATH = '/sys/module/tuxedo_keyboard'
    VERSION = '0.7'

    modes = (
        'color',
        'breathe',
        'cycle',
        'dance',
        'flash',
        'random',
        'tempo',
        'wave'
    )

    colors = colors
    regions = ('left', 'center', 'right', 'extra')
    params = ('state', 'mode', 'color_left', 'color_center', 'color_right', 'color_extra', 'brightness')

    @staticmethod
    def get_device_param(prop):
        """ read driver param value directly from '/sys/devices/platform/tuxedo_keyboard/' """

        if os.path.isfile(BacklightControl.DEVICE_PATH + prop):
            return open(BacklightControl.DEVICE_PATH + prop).read()
        return None

    @staticmethod
    def get_device_color(region):
        """ read driver color value directly from '/sys/devices/platform/tuxedo_keyboard/' """

        color = BacklightControl.get_device_param('color_' + region)
        if color:
            try:
                index = list(BacklightControl.colors.values()).index(color.strip().upper())
                return list(BacklightControl.colors.keys())[index]
            except Exception:
                return 'Select...'
        return None

    @staticmethod
    def set_device_param(prop, value):
        fh = open(BacklightControl.DEVICE_PATH + prop, mode='r+')
        fh.write(str(value))
        fh.close()

    @staticmethod
    def set_device_color(region, color):
        if color in BacklightControl.colors.keys():
            index = list(BacklightControl.colors.values()).index(color.strip().upper())
            values = list(BacklightControl.colors.keys())
            BacklightControl.set_device_param('color_' + region, values[index])

    @staticmethod
    def find_color_by_key(color):
        index = list(BacklightControl.colors.keys()).index(color)
        return '0x' + list(BacklightControl.colors.values())[index]

    @staticmethod
    def is_single_color():
        """ checks whether all keyboard regions have the same color assigned to them """
        is_single = True
        last_color = None

        for region in BacklightControl.regions:
            color = BacklightControl.get_device_color(region)
            if last_color not in (None, color):
                is_single = False
                break
            else:
                last_color = color

        return is_single

    @staticmethod
    def set_single_color(color):
        """ assigns a single color by name to all keyboard regions """
        for region in BacklightControl.regions:
            mapped_color = BacklightControl.find_color_by_key(color)
            BacklightControl.set_device_param('color_' + region, mapped_color)

    @staticmethod
    def capitalize(label):
        """ capitalizes a string """
        return label.capitalize()

    @property
    def state(self):
        param = self.get_device_param('state')
        if param:
            return int(param)
        return 1

    @state.setter
    def state(self, value):
        self.set_device_param('state', value)

    @property
    def mode(self):
        param = self.get_device_param('mode')
        if param and len(self.modes) > int(param):
            return self.modes[int(param)]
        return None

    @mode.setter
    def mode(self, value):
        index = self.modes.index(value)
        self.set_device_param('mode', index)

    @property
    def color_left(self):
        """ get hex code for color_left """
        return self.get_device_color('left')

    @color_left.setter
    def color_left(self, value):
        """ set hex code for color_left, with color name present in colors dict """
        self.set_device_param('color_left', self.find_color_by_key(value))

    @property
    def color_center(self):
        """ get hex code for color_center """
        return self.get_device_color('center')

    @color_center.setter
    def color_center(self, value):
        """ set hex code for color_center, with color name present in colors dict """
        self.set_device_param('color_center', self.find_color_by_key(value))

    @property
    def color_right(self):
        """ get hex code for color_right """
        return self.get_device_color('right')

    @color_right.setter
    def color_right(self, value):
        """ set hex code for color_right, with color name present in colors dict """
        self.set_device_param('color_right', self.find_color_by_key(value))

    @property
    def color_extra(self):
        """ get hex code for color_extra """
        return self.get_device_color('extra')

    @color_extra.setter
    def color_extra(self, value):
        """ set hex code for color_extra, with color name present in colors dict """
        self.set_device_param('color_extra', self.find_color_by_key(value))

    @property
    def brightness(self):
        """ get brightness value """
        return self.get_device_color('extra')

    @color_extra.setter
    def color_extra(self, value):
        """ set hex code for color_extra, with color name present in colors dict """
        self.set_device_param('color_extra', self.find_color_by_key(value))


    @staticmethod
    def display_modes():
        """ return a capitalized item-list of all backlight modes """
        return map(BacklightControl.capitalize, BacklightControl.modes)

    @staticmethod
    def display_colors():
        """ return a capitalized item-list of all backlight colors """
        return map(BacklightControl.capitalize, BacklightControl.colors.keys())

backlight = BacklightControl()

