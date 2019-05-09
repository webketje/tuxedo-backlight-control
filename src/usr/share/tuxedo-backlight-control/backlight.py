import os
from io import StringIO
from colors import colors

dirname = os.path.dirname(__file__)


class BacklightControl():
    DEVICE_PATH = '/sys/devices/platform/tuxedo_keyboard/'
    MODULE_PATH = '/sys/module/tuxedo_keyboard'

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
    regions = ('left','center','right','extra')
    params = ('state','mode','color_left','color_center','color_right','color_extra')

    @staticmethod
    def get_device_param(prop):
        if os.path.isfile(BacklightControl.DEVICE_PATH + prop):
            return open(BacklightControl.DEVICE_PATH + prop).read()

    @staticmethod
    def get_device_color(region):
        color = BacklightControl.get_device_param('color_' + region)
        if color:
            index = list(BacklightControl.colors.values()).index(color.strip().upper())
            return list(BacklightControl.colors.keys())[index]

    @staticmethod
    def set_device_param(prop, value):
        fh = open(BacklightControl.DEVICE_PATH + prop, mode='r+')
        fh.write(str(value))
        fh.close()

    @staticmethod
    def set_device_color(region, color):
        if color in BacklightControl.colors.keys():
            index = list(BacklightControl.colors.values()).index(color.strip().upper())
            BacklightControl.set_device_param('color_' + region, list(BacklightControl.colors.keys())[index])

    @staticmethod
    def find_color_by_key(color):
        index = list(BacklightControl.colors.keys()).index(color)
        return '0x' + list(BacklightControl.colors.values())[index]

    @staticmethod
    def is_single_color():
        is_single = True
        last_color = None

        for region in BacklightControl.regions:
            color = BacklightControl.get_device_color(region)
            if last_color != None and last_color != color:
                is_single = False
                break
            else:
              last_color = color

        return is_single
    
    @staticmethod
    def set_single_color(color):
        for region in BacklightControl.regions:
            BacklightControl.set_device_color(region, color)

    @staticmethod
    def capitalize(label):
        return label.capitalize()

    @property
    def state(self):
        param = self.get_device_param('state')
        if param:
            return int(param)
        return 1

    @state.setter
    def state(self, value):
        BacklightControl.set_device_param('state', value)
    
    @property
    def mode(self):
        param = self.get_device_param('mode')
        if param and len(self.modes) > int(param):
            return self.modes[int(param)]

    @mode.setter
    def mode(self, value):
        print(value)
        index = BacklightControl.modes.index(value)
        BacklightControl.set_device_param('mode', index)

    @property
    def color_left(self):
       return BacklightControl.get_device_color('left')

    @color_left.setter
    def color_left(self, value):
        BacklightControl.set_device_param('color_left', BacklightControl.find_color_by_key(value))

    @property
    def color_center(self):
       return BacklightControl.get_device_color('center')

    @color_center.setter
    def color_center(self, value):
        BacklightControl.set_device_param('color_center', BacklightControl.find_color_by_key(value))

    @property
    def color_right(self):
       return BacklightControl.get_device_color('right')

    @color_right.setter
    def color_right(self, value):
        BacklightControl.set_device_param('color_right', BacklightControl.find_color_by_key(value))

    @property
    def color_extra(self):
       return BacklightControl.get_device_color('extra')

    @color_extra.setter
    def color_extra(self, value):
        BacklightControl.set_device_param('color_extra', BacklightControl.find_color_by_key(value))

    def display_modes(self):
        return map(BacklightControl.capitalize, self.modes)

    def display_colors(self):
        return map(BacklightControl.capitalize, self.colors.keys())

backlight = BacklightControl()