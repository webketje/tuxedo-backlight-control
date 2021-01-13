#!/usr/bin/pkexec /usr/bin/python3

import tkinter as tk
from tkinter import ttk
from backlight_control import backlight


class App(ttk.Frame):

    ICONPATH = '/usr/share/tuxedo-backlight-control/icon.png'

    bgcolor = '#333333'  # background
    fgcolor = '#AAAAAA'  # foreground
    hlcolor = '#DDDDDD'  # highlight
    shcolor = '#666666'  # shade

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.init_ttk_style()
        self.parent = parent
        self.parent.title('Tuxedo Backlight Ctrl')
        self.parent.iconphoto(parent._w, tk.PhotoImage(file=self.ICONPATH))
        self.parent.resizable(width=False, height=False)
        self.parent.grid(widthInc=8, heightInc=8, baseHeight=5, baseWidth=40)
        self.parent.grid_columnconfigure(0, weight=1, pad=2)
        self.parent.grid_rowconfigure(0, weight=1, pad=2)

        self.regions = (
            'color_left',
            'color_center',
            'color_right'
        )
        if backlight.color_extra:
        	self.regions.append('color_extra')

        self.bg_frame = ttk.Frame(self.parent)
        self.bg_frame.grid(sticky=tk.NSEW, column=0, row=0)
        self.bg_frame.grid_columnconfigure(0, weight=1, minsize=150, pad=10)
        self.bg_frame.grid_columnconfigure(1, weight=2, minsize=150, pad=10)
        self.bg_frame.grid_rowconfigure(0, weight=0, pad=10)
        self.bg_frame.grid_rowconfigure(1, weight=0, pad=10)
        self.bg_frame.grid_rowconfigure(2, weight=0, pad=10)
        self.bg_frame.grid_rowconfigure(6, weight=0, pad=0)

        for region in enumerate(self.regions):
            self.bg_frame.grid_rowconfigure(region[0] + 2, weight=0, pad=10)

        self.labels = {
            'mode': ttk.Label(self.bg_frame, text='Backlight mode: '),
            'color': ttk.Label(self.bg_frame, text='Backlight color: '),
            'color_mode': ttk.Label(self.bg_frame, text='Color mode: '),
            'color_left': ttk.Label(self.bg_frame, text='Color left: '),
            'color_center': ttk.Label(self.bg_frame, text='Color center: '),
            'color_right': ttk.Label(self.bg_frame, text='Color right: '),
            'color_extra': ttk.Label(self.bg_frame, text='Color extra: ')
        }

        if backlight.state == 1:
            initial_mode = backlight.mode.capitalize()
        else:
            initial_mode = 'Select...'

        self.values = {
            'mode': tk.StringVar(self, value=initial_mode),
            'color_mode': tk.StringVar(self, value=self.color_mode),
            'color_left': tk.StringVar(self, value=backlight.color_left.capitalize()),
            'color_center': tk.StringVar(self, value=backlight.color_center.capitalize()),
            'color_right': tk.StringVar(self, value=backlight.color_right.capitalize()),
        }
        if backlight.color_extra:
        	self.values.color_extra = tk.StringVar(self, value=backlight.color_extra.capitalize())

        def set_single_color(color):
            if not color == 'Select...':
                self.color = color

        self.widgets = {
            'mode': ttk.OptionMenu(
                self.bg_frame,
                self.values['mode'],
                None,
                *backlight.display_modes(),
                command=self.on_mode_switch
            ),
            'color': ttk.OptionMenu(
                self.bg_frame,
                self.values['color_left'],
                self.color_left,
                *backlight.display_colors(),
                command=set_single_color
            ),
            'color_mode': {'frame':ttk.Frame(self.bg_frame)},
            'color_left': ttk.OptionMenu(
                self.bg_frame,
                self.values['color_left'],
                self.color_left,
                *backlight.display_colors(),
                command=self.color_setter('left')
            ),
            'color_center': ttk.OptionMenu(
                self.bg_frame,
                self.values['color_center'],
                backlight.color_center.capitalize(),
                *backlight.display_colors(),
                command=self.color_setter('center')
            ),
            'color_right': ttk.OptionMenu(
                self.bg_frame,
                self.values['color_right'],
                backlight.color_right.capitalize(),
                *backlight.display_colors(),
                command=self.color_setter('right')
            )
        }
        if backlight.color_extra:
            self.widgets.color_extra: ttk.OptionMenu(
                self.bg_frame,
                self.values['color_extra'],
                backlight.color_extra.capitalize(),
                *backlight.display_colors(),
                command=self.color_setter('extra')
            )

        def cmd():
            self.on_color_mode_switch(self.values['color_mode'].get())

        self.widgets['color_mode']['options']=(
            ttk.Radiobutton(
                self.widgets['color_mode']['frame'],
                variable=self.values['color_mode'],
                text='Single', value='single',
                command=cmd
            ),
            ttk.Radiobutton(
                self.widgets['color_mode']['frame'],
                variable=self.values['color_mode'],
                text='Multiple', value='multiple',
                command=cmd
            )
        )

        menuconfig = {
            'relief': tk.FLAT,
            'background': App.bgcolor,
            'activebackground': App.shcolor,
            'activeborderwidth': 0,
            'foreground': App.fgcolor,
            'bd': 0,
            'activeforeground': App.hlcolor
        }

        self.widgets['mode']['menu'].config(**menuconfig)
        self.widgets['color']['menu'].config(**menuconfig)
        self.widgets['color_left']['menu'].config(**menuconfig)
        self.widgets['color_center']['menu'].config(**menuconfig)
        self.widgets['color_right']['menu'].config(**menuconfig)
        
        if backlight.color_extra:
            self.widgets['color_extra']['menu'].config(**menuconfig)

        self.labels['mode'].grid(column=0, row=0, sticky='EW')
        self.widgets['mode'].grid(column=1, row=0, sticky='EW', padx=10)
        self.init_footer()

        if backlight.state == 1:
            self.init_mode(backlight.mode)
        else:
            self.backlight_off()

    def init_ttk_style(self):
        ttk_style = ttk.Style()
        ttk_style.theme_use('clam')
        ttk_style.configure(
            '.',
            background=App.bgcolor,
            activebackground=App.shcolor,
            indicatoron=0,
            foreground=App.fgcolor,
            bordercolor=App.shcolor,
            highlightthickness=0,
            highlightcolor=App.hlcolor,
            relief=tk.FLAT
        )
        ttk_style.configure(
            'TButton',
            background=App.bgcolor,
            bordercolor=App.shcolor,
            relief=tk.SOLID,
            highlightcolor=App.hlcolor
        )
        ttk_style.configure(
            'TMenubutton',
            borderwidth=1,
            bordercolor=App.shcolor,
            relief=tk.SOLID
        )
        ttk_style.configure('TRadiobutton', background=App.bgcolor)
        ttk_style.configure('TMenu', background=App.bgcolor)
        ttk_style.configure('TLabel', padding=5, foreground=App.fgcolor)
        ttk_style.map(
            '.',
            background=[
                ('active', App.shcolor),
                ('focus', App.shcolor)
            ],
            foreground=[
                ('active', App.hlcolor),
                ('focus', App.hlcolor),
                ('disabled', App.shcolor)
            ],
            bordercolor=[
                ('active', App.shcolor)
            ]
        )
        ttk_style.map(
            'TButton',
            background=[('active', App.shcolor)],
            foreground=[('disabled', App.shcolor)],
            bordercolor=[('disabled', '#4444444')]
        )

    def color_setter(self, region):
        return lambda val: setattr(backlight, 'color_' + region, val.lower())

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
        self.widgets['color_mode']['options'][0].grid(
            row=1,
            column=0,
            sticky=tk.EW
        )
        self.widgets['color_mode']['options'][1].grid(
            row=1,
            column=1,
            sticky=tk.EW
        )

    def on_color_mode_switch(self, value):
        if value == 'multiple':
            self.hide_single_color()
            self.init_multiple_colors()
        else:
            if self.values['color_left'].get() != 'Select...':
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
        self.off_button.configure(state='enabled')
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
        if not value == 'Select...':
            backlight.color_left = value.lower()

    def backlight_off(self):
        self.off_button.configure(state='disabled')
        backlight.state = 0
        self.values['mode'].set('Select...')
        self.hide_colors()

    def init_footer(self):
        state = 'disabled' if not backlight.state else 'enabled'
        self.off_button = ttk.Button(
            self.bg_frame,
            text="Backlight off",
            command=self.backlight_off,
            state=state
        )
        self.off_button.grid(sticky=tk.E, column=1, row=6, padx=10, pady=10)


def init():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    init()
