#!/usr/bin/env python3

import tkinter as tk
import os, configparser, subprocess
from io import StringIO

dirname = os.path.dirname(__file__)

def bash(cmd):
    subprocess.call(['bash', os.path.join(dirname, 'bin/backlight'), *cmd])

class BacklightManager():
    def __init__(self):
        self.readconf()

    def readconf(self):
        self.config = configparser.ConfigParser()
        self.read_backlight_cfg()
        # see https://stackoverflow.com/questions/9686184/is-there-a-version-of-configparser-that-deals-with-files-with-no-section-headers
        options = StringIO(u'[commands]\n%s' % open(os.path.join(dirname, 'commands')).read())
        colors = StringIO(u'[colors]\n%s' % open(os.path.join(dirname, 'colors')).read())
        self.config.read_file(options)
        self.config.read_file(colors)

    def valid_backlight_cfg(self, cfg):
        return cfg.startswith('options tuxedo_keyboard ')

    def read_backlight_cfg(self):
        if os.path.isfile('/etc/modprobe.d/tuxedo_keyboard.conf'):
            contents = open('/etc/modprobe.d/tuxedo_keyboard.conf').read()

            if self.valid_backlight_cfg(contents):
                contents = contents.split('options tuxedo_keyboard ')[1].strip()
                current = StringIO(u'[current]\n%s' % '\n'.join(contents.split(' ')))
                self.config.read_file(current)

    def write_backlight_cfg(self):
        return 'test'

    def display_commands(self):
        cmds = self.config['commands'].keys()
        labels = []
        for cmd in cmds:
           labels.append(cmd.capitalize())
        return labels

    def is_color():
        if 'mode' in self.config['current'].keys():
            return self.config['current'].getint('mode') == 0

    def is_off(self):
        if 'state' in self.config['current'].keys():
            return self.config['current'].getint('state') == 0

    def mode(self):
        if 'mode' in self.config['current'].keys():
            return self.config['current'].getint('mode')

    def color(self):
        if 'color_left' not in self.config['current'].keys():
            return

        color_left = self.config['current'].get('color_left')
        colors = self.config.items('colors')

        for color in colors:
            hex = color[1].replace('\'', '')
            if hex == color_left.replace('0x', ''):
                return color[0]

    def set_command(self, *args):
        bash(args)

class Window(tk.Frame):
    def __init__(self, master=None):
        self.master = master
        self.master.title('Tuxedo Backlight Ctrl')
        self.master.resizable(width=False, height=False)
        self.master.geometry('280x150')
        self.master.wm_iconbitmap('@/usr/share/tuxedo-backlight-control/icon.xbm')
        self.backlight = BacklightManager()
        self.initialize_user_interface()

    def close(self):
        self.master.destroy()

    def on_backlight_off(self):
        self.backlight.set_command('off')

        # side effects
        self.off_button.configure(state='disabled', relief='sunken')
        self.colors.configure(state='disabled')
        self.selected_color.set('Select...')
        self.selected_option.set('Select...')

    def toggle_off_button(self, **enabled):
        backlight_state_off = {
            'text'   : 'Backlight off',
            'relief' : 'sunken',
            'state'  : 'disabled',
            'command': self.on_backlight_off
        }
        backlight_state_on = {
            'text'   : 'Backlight off',
            'relief' : 'raised',
            'state'  : 'normal',
            'command': self.on_backlight_off
        }

        if not enabled:
            self.off_button.configure(**backlight_state_off)
        else:
            self.off_button.configure(**backlight_state_on)

    def initialize_user_interface(self):
        self.main_frame = tk.Frame(self.master, width=400, height=300, padx=8, pady=8)
        self.main_frame.grid_propagate(0)
        self.footer_frame = tk.Frame(self.master, padx=8, pady=8)
        self.entry=tk.Entry(self.master)

        self.off_button = tk.Button(self.footer_frame)
        self.toggle_off_button(enabled=self.backlight.is_off())

        self.off_button.pack(side=tk.LEFT, anchor="w")
        self.close_button=tk.Button(self.footer_frame, text='Close', relief="groove", command=self.close)
        self.close_button.pack(side=tk.LEFT, anchor="e")

        options = self.backlight.display_commands()
        self.options_frame = tk.Frame(self.main_frame, width=300)
        self.selected_option = tk.StringVar(self.master)

        if type(self.backlight.mode()) == int:
            self.selected_option.set(options[self.backlight.mode()])
        else:
            self.selected_option.set('Select...')

        self.options_label = tk.Label(self.options_frame, text='Backlight mode:')
        self.options = tk.OptionMenu(self.options_frame, self.selected_option, *options, command=self.on_option_select)
        self.options_label.pack(padx=5, pady=5, side=tk.LEFT, anchor="w")
        self.options.pack(
            padx=5,
            pady=5,
            side=tk.RIGHT,
            anchor="e",
            fill="x",
            expand=True
        )

        self.options_frame.pack(side="top", fill="both", expand=False)
        self.init_colors()

        self.main_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.footer_frame.grid_rowconfigure(1, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def init_colors(self):
        self.colors_frame = tk.Frame(self.main_frame, width=300)
        self.selected_color = tk.StringVar(self.master)
        self.colors = tk.OptionMenu(self.colors_frame, self.selected_color, *self.backlight.config['colors'].keys(), command=self.on_color_select)

        if self.backlight.color():
            self.selected_color.set(self.backlight.color())
            self.colors.configure(state='normal')
        else:
            self.selected_color.set('Select...')
            self.colors.configure(state='disabled')

        self.colors_label = tk.Label(self.colors_frame, text='Backlight color:')

        self.colors_label.pack(padx=5, pady=5, side=tk.LEFT, anchor="w")
        self.colors.pack(padx=5, pady=5, side=tk.RIGHT, anchor="e", fill="x", expand=True)
        self.colors_frame.pack(side="top", fill="both", expand=False)

    def on_option_select(self, sel_opt):
        if not sel_opt.lower() in self.backlight.config['commands']:
            return

        if sel_opt == 'Color':
            self.colors.configure(state = 'normal')
            self.toggle_off_button(enabled=False)
        else:
            self.colors.configure(state = 'disabled')
            self.toggle_off_button(enabled=True)
            self.selected_color.set('Select...')

        if sel_opt.lower() in self.backlight.config['commands'] and not sel_opt == 'Color':
            self.backlight.set_command(sel_opt.lower())

    def on_color_select(self, *args):
        sel_color = self.selected_color.get()

        if sel_color.lower() in self.backlight.config['colors']:
            self.backlight.set_command(self.selected_option.get().lower(), sel_color.lower())
            self.toggle_off_button(enabled=True)

root = tk.Tk()
app = Window(root)
root.mainloop()
