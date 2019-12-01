# TUXEDO Backlight Control
Minimal Linux distro CLI &amp; UI for TUXEDO / Clevo computers Keyboard Backlight

This utility automates toggling keyboard backlight state for TUXEDO / Clevo computers on Linux.
It can toggle the keyboard backlight off, set any modes defined [here](https://github.com/tuxedocomputers/tuxedo-keyboard#modes) and set a single or multiple colors in Color (`custom`)  mode.
Available colors can be found [here](https://www.cssportal.com/html-colors/orig-16-colors.php).

## Usage

### UI

Search for *TUXEDO Backlight Control* from the <kbd>Super</kbd> (Start) menu.

![](/assets/screenshot.png)

### CLI

```
backlight <command> [<option>]
```

```
Usage:
    -h, --help            Display this message

    ui                    Start the TUXEDO Backlight Control UI

    off                   Turn off keyboard backlight

    <mode>                Set the keyboard backlight to <mode>, one of:
                          breathe, cycle, dance, flash, random, tempo, wave

    color  <color>{1,4}   Set the keyboard backlight to a single color, one of:
                          white, silver, gray, yellow, orange, red, maroon, crimson,
                          fuchsia, purple, rose, cyan, turquoise, teal, blue, navy,
                          olive, lime, green,
                          OR any valid colors defined in /etc/tuxedo-backlight-control/colors.conf

                          Alternatively, set the keyboard to 4 distinct colors,
                          in the order: left, center, right, extra. Only regions supported
                          by your keyboard will have effect.
```

### Custom Colors

As of 0.5 you can add your own custom colors, by creating a `colors.conf` file in a directory `/etc/tuxedo-backlight-control`. The file should have a format like:

```
my_color1=123456
my_color2=654321
```

The colors added here will be usable both in the CLI, and appear in the color dropdown in the UI.
The values should be valid HEX colors, the keys can only contain alphanumeric characters. 

Development of this software is done on Clevo N150-ZU / N151-ZU. Only single color mode is known to work for these the models.

## Requirements

Required packages: 

* On **Debian/ Ubuntu/ Linux Mint** : python3, python3-tk & policykit-1.
* On **Arch Linux** : python, tk, polkit

On Debian you can verify if you have these by doing `apt show <package-name>`.  

Required modules: [tuxedo-keyboard](https://github.com/tuxedocomputers/tuxedo-keyboard)  
Download it from the repository or git clone as below:

```
git clone https://github.com/tuxedocomputers/tuxedo-keyboard.git
cd tuxedo-keyboard
```

Follow the instructions at [tuxedo-keyboard under the section "The DKMS route"](https://github.com/tuxedocomputers/tuxedo-keyboard#the-dkms-route)

## Alternative options

### On Arch Linux:

You can install the ["tuxedo-keyboard"](https://aur.archlinux.org/packages/tuxedo-keyboard/ "TUXEDO Keyboard AUR Package") Package from the AUR

### On Ubuntu (Linux Mint and Debian are not tested)

You can download and install the TUXEDO Keyboard .deb Package from http://deb.tuxedocomputers.com/ubuntu/pool/main/t/tuxedo-keyboard-dkms/

----

## Install

*Note: You might have to execute some of the commands below with `sudo`*

### Debian

Download and double-click the `.deb` package from the [releases](https://github.com/webketje/tuxedo-backlight-control/releases/latest), or run
```
sudo dpkg -i tuxedo-backlight-control_0.6-1_amd64.deb
```
from the folder where you downloaded it.

### Arch Linux

Download the `.pkg.tar.xz` package from the [releases](https://github.com/webketje/tuxedo-backlight-control/releases/latest), and run

```
pacman -U tuxedo-backlight-control-0.6-1-any.pkg.tar.xz
```
from the folder where you downloaded it.

_Note: Although it is not recommended, you **can** install dpkg on Arch Linux, and install the .deb package there as you would on Debian OS'es._

Alternatively, you can use the [AUR Package](https://aur.archlinux.org/packages/tuxedo-backlight-control/) from [Steven Seifried](https://github.com/StevenSeifried/)

### Manual

```
git clone https://github.com/webketje/tuxedo-backlight-control.git
cd tuxedo-backlight-control
./pack.sh
```

In the `dist` folder you will find distribution packages built for the supported distro's. If none of these packages fits your distribution you can manually paste the contents of the `src/` folder in your system root like so:

```
cd src
cp -r usr /usr
ln -s -f -T /usr/share/tuxedo-backlight-control/backlight.py /usr/local/bin/backlight
```



## Uninstall

*Note: You might have to execute some of the commands below with `sudo`*

### Debian

```
dpkg -r tuxedo-backlight-control
```

### Arch Linux

```
pacman -Rs tuxedo-backlight-control
```

### Manual

```
rm -rf /usr/share/tuxedo-backlight-control
unlink /usr/local/bin/backlight
unlink /usr/share/doc/tuxedo-backlight-control/copyright
unlink /usr/share/applications/tuxedo-backlight-control.desktop
unlink /usr/share/polkit-1/actions/webketje.tuxedo-backlight-control.policy
```


