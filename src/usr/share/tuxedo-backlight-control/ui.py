#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import os
from backlight import backlight

class App(ttk.Frame):

    bgcolor = '#333333'  # background
    fgcolor = '#AAAAAA'  # foreground
    hlcolor = '#DDDDDD'  # highlight
    shcolor = '#666666'  # shade

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.init_ttk_style()

        self.parent = parent
        self.parent.title('Tuxedo Backlight Ctrl')
        self.parent.wm_iconbitmap('@/usr/share/tuxedo-backlight-control/icon.xbm')
        self.parent.resizable(width=False, height=False)
        self.parent.grid(widthInc=8, heightInc=8, baseHeight=5, baseWidth=40)
        self.parent.grid_columnconfigure(0, weight=1, pad=2)
        self.parent.grid_rowconfigure(0, weight=1, pad=2)

        self.regions = ('color_left', 'color_center', 'color_right', 'color_extra')

        self.bgFrame = ttk.Frame(self.parent)
        self.bgFrame.grid(sticky=tk.NSEW, column=0, row=0)
        self.bgFrame.grid_columnconfigure(0, weight=1, minsize=150, pad=10)
        self.bgFrame.grid_columnconfigure(1, weight=2, minsize=150, pad=10)
        self.bgFrame.grid_rowconfigure(0, weight=0, pad=10)
        self.bgFrame.grid_rowconfigure(1, weight=0, pad=10)
        self.bgFrame.grid_rowconfigure(2, weight=0, pad=10)
        self.bgFrame.grid_rowconfigure(6, weight=0, pad=0)

        for index, region in enumerate(self.regions):
            self.bgFrame.grid_rowconfigure(index + 2, weight=0, pad=10)

        self.labels = dict(
            mode = ttk.Label(self.bgFrame, text='Backlight mode: '),
            color = ttk.Label(self.bgFrame, text='Backlight color: '),
            color_mode = ttk.Label(self.bgFrame, text='Color mode: '),
            color_left = ttk.Label(self.bgFrame, text='Color left: '),
            color_center = ttk.Label(self.bgFrame, text='Color center: '),
            color_right = ttk.Label(self.bgFrame, text='Color right: '),
            color_extra = ttk.Label(self.bgFrame, text='Color extra: ')
        )

        self.values = dict(
            mode = tk.StringVar(self, value = backlight.mode.capitalize()),
            color_mode = tk.StringVar(self, value = self.color_mode),
            color_left = tk.StringVar(self, value = backlight.color_left.capitalize()),
            color_center = tk.StringVar(self, value = backlight.color_center.capitalize()),
            color_right = tk.StringVar(self, value = backlight.color_right.capitalize()),
            color_extra = tk.StringVar(self, value = backlight.color_extra.capitalize())
        )

        def set_single_color(color):
            self.color = color

        self.widgets = dict(
            mode = ttk.OptionMenu(self.bgFrame, self.values['mode'], None, *backlight.display_modes(), command = self.on_mode_switch),
            color = ttk.OptionMenu(self.bgFrame, self.values['color_left'], self.color_left, *backlight.display_colors(), command = set_single_color),
            color_mode = dict(frame = ttk.Frame(self.bgFrame)),
            color_left = ttk.OptionMenu(self.bgFrame, self.values['color_left'], self.color_left, *backlight.display_colors(), command = self.color_setter('left')),
            color_center = ttk.OptionMenu(self.bgFrame, self.values['color_center'], backlight.color_center.capitalize(), *backlight.display_colors(), command = self.color_setter('center')),
            color_right = ttk.OptionMenu(self.bgFrame, self.values['color_right'], backlight.color_right.capitalize(), *backlight.display_colors(), command = self.color_setter('right')),
            color_extra = ttk.OptionMenu(self.bgFrame, self.values['color_extra'], backlight.color_extra.capitalize(), *backlight.display_colors(), command = self.color_setter('extra'))
        )

        self.widgets['color_mode']['options'] = (
            ttk.Radiobutton(self.widgets['color_mode']['frame'], variable=self.values['color_mode'], text='Single', value='single', command = lambda : self.on_color_mode_switch(self.values['color_mode'].get())),
            ttk.Radiobutton(self.widgets['color_mode']['frame'], variable=self.values['color_mode'], text='Multiple', value='multiple', command = lambda : self.on_color_mode_switch(self.values['color_mode'].get()))
        )

        menuconfig = dict(
            relief=tk.FLAT,
            background=App.bgcolor,
            activebackground=App.shcolor,
            activeborderwidth=0,
            foreground=App.fgcolor,
            bd=0,
            activeforeground=App.hlcolor
        )

        self.widgets['mode']['menu'].config(**menuconfig)
        self.widgets['color']['menu'].config(**menuconfig)
        self.widgets['color_left']['menu'].config(**menuconfig)
        self.widgets['color_center']['menu'].config(**menuconfig)
        self.widgets['color_right']['menu'].config(**menuconfig)
        self.widgets['color_extra']['menu'].config(**menuconfig)

        self.labels['mode'].grid(column=0, row=0, sticky='EW')
        self.widgets['mode'].grid(column=1, row=0, sticky='EW', padx=10)
        self.init_footer()
        self.init_mode(backlight.mode)
        self.backlight_toggle()

    def init_ttk_style(self):
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('clam')
        ttkStyle.configure('.', background=App.bgcolor, activebackground=App.shcolor, indicatoron=0,
                           foreground=App.fgcolor, bordercolor=App.shcolor, highlightthickness=0, highlightcolor=App.hlcolor, relief=tk.FLAT)
        ttkStyle.configure('TButton', background=App.bgcolor, bordercolor=App.shcolor, relief=tk.SOLID, highlightcolor=App.hlcolor)
        ttkStyle.configure('TMenubutton', borderwidth=1, bordercolor=App.shcolor, relief=tk.SOLID)
        ttkStyle.configure('TRadiobutton', background=App.bgcolor)
        ttkStyle.configure('TMenu', background=App.bgcolor)
        ttkStyle.configure('TLabel', padding=5, foreground=App.fgcolor)
        ttkStyle.map('.',
            background=[('active', App.shcolor),
                        ('focus', App.shcolor)],
            foreground=[('active', App.hlcolor),
                        ('focus', App.hlcolor),
                        ('disabled', App.shcolor)],
            bordercolor=[('active', App.shcolor)]
        )
        ttkStyle.map('TButton', background=[('active', App.shcolor)], foreground=[('disabled', App.shcolor)], bordercolor=[('disabled', '#4444444')])

    def color_setter(self, region):
        return lambda value: setattr(backlight, 'color_' + region, value.lower())

    def init_colors(self):
        fmt = self.color_mode
        self.init_color_mode_radio()
        if fmt == 'single':
            self.init_single_color()
        else:
            self.init_multiple_colors()

    def hide_multiple_colors(self):
        for region in self.regions:
            self.labels[region].grid_remove()
            self.widgets[region].grid_remove()
    
    def hide_single_color(self):
        self.labels['color'].grid_remove()
        self.widgets['color'].grid_remove()

    def hide_colors(self):
        self.widgets['color_mode']['frame'].grid_remove()
        self.labels['color_mode'].grid_remove()
        self.hide_single_color()
        self.hide_multiple_colors()

    def init_color_mode_radio(self):
        self.values['color_mode'].set(self.color_mode)
        self.labels['color_mode'].grid(row=1, column=0, sticky=tk.EW)
        self.widgets['color_mode']['frame'].grid(row=1, column=1, sticky=tk.EW)
        self.widgets['color_mode']['options'][0].grid(row=1, column=0, sticky=tk.EW)
        self.widgets['color_mode']['options'][1].grid(row=1, column=1, sticky=tk.EW)

    def on_color_mode_switch(self, value):
        if value == 'multiple':
            self.hide_single_color()
            self.init_multiple_colors()
        else:
            self.color = self.color_left
            self.hide_multiple_colors()
            self.init_single_color()

    def init_single_color(self):
        self.labels['color'].grid(column=0, row=2, sticky='EW')
        self.widgets['color'].grid(column=1, row=2, sticky='EW', padx=10)

    def init_multiple_colors(self):
        for index, region in enumerate(self.regions):
            row = index + 2
            from_device = getattr(backlight, region)
            self.labels[region].grid(column=0, row=row, sticky='EW')
            self.values[region].set(from_device.capitalize())
            self.widgets[region].grid(column=1, row=row, sticky='EW', padx=10)

    def init_mode(self, mode):
        if mode == 'color':
            self.init_colors()
        else:
            self.hide_colors()

    def on_mode_switch(self, value):
        backlight.state = 1
        self.offButton.configure(state='enabled')
        self.init_mode(value.lower())
        self.mode = value

    @property
    def mode(self):
        return backlight.mode.capitalize()

    @mode.setter
    def mode(self, value):
        self.values['mode'].set(value)
        backlight.mode = value.lower()

    @property
    def color_mode(self):
        return 'single' if backlight.is_single_color() else 'multiple'

    @property
    def color(self):
        return backlight.color_left.capitalize()

    @color.setter
    def color(self, value):
        for region in self.regions:
            self.values[region].set(value)
            setattr(backlight, region, value.lower())

    @property
    def color_left(self):
        return backlight.color_left.capitalize()

    @color_left.setter
    def color_left(self, value):
        self.values['color_left'].set(value)
        backlight.color_left = value.lower()


    def backlight_toggle(self):
        if backlight.state == 1:
            self.offButton.configure(state='disabled')
            backlight.state = 0
            self.values['mode'].set('Select...')
            self.hide_colors()


    def init_footer(self):
        state = 'disabled' if not backlight.state else 'enabled'
        self.offButton = ttk.Button(self.bgFrame, text="Backlight off", command=self.backlight_toggle, state=state)
        self.offButton.grid(sticky=tk.E, column=1, row=6, padx=10, pady=10)


if __name__ == '__main__':
    root = tk.Tk()
    run = App(root)
    root.mainloop()
