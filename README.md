# Tuxedo Backlight Control
Minimal Linux distro CLI &amp; UI for TUXEDO / Clevo computers Keyboard Backlight

This utility automates toggling keyboard backlight state for Tuxedo/ Clevo computers on Linux.
It can toggle the keyboard backlight off, set any modes defined [here](https://github.com/tuxedocomputers/tuxedo-keyboard#modes) and set a single-color subset from the `custom` mode.  
Available colors can be found [here](https://www.cssportal.com/html-colors/orig-16-colors.php).

## Usage

### UI

Search for *Tuxedo Backlight Control* from the <kbd>Super</kbd> (Start) menu.

![](/assets/screenshot.png)

### CLI

```
backlight <command> [<option>]
```

```
Usage:
    -h, --help        Display this message

    ui                Start the Tuxedo Backlight Control UI

    off               Turn off keyboard backlight

    <mode>            Set the keyboard backlight to <mode>, one of:
                      breathe, cycle, dance, flash, random, tempo, wave

    color             Set the keyboard backlight to a single color, one of:
                      white, silver, gray, yellow, orange, red, maroon, crimson,
                      fuchsia, purple, rose, cyan, turquoise, teal, blue, navy,
                      olive, lime, green

```

## Requirements

You need bash for the CLI (pre-installed on most Linux distros) and python3 and python3-tk for the GUI.
You also need the [tuxedo-keyboard](https://github.com/tuxedocomputers/tuxedo-keyboard) module installed.
Download it from the repository or git clone as below:

```
git clone https://github.com/tuxedocomputers/tuxedo-keyboard.git
cd tuxedo-keyboard
```

Follow the instructions at [tuxedo-keyboard under the section "The DKMS route"](https://github.com/tuxedocomputers/tuxedo-keyboard#the-dkms-route)

## Install

Download and double-click the `.deb` package from the [releases](https://github.com/webketje/tuxedo-backlight-control/releases).
Or do it manually:

```
git clone https://github.com/webketje/tuxedo-backlight-control.github
cd tuxedo-backlight-control
./pack.sh
sudo dpkg -i tuxedo-backlight-control.deb
```

## Uninstall

```
sudo dpkg -r tuxedo-backlight-control
```
