# DashPi

[![Version][version-image]][version-url]
[![License][license-image]][license-url]
[![Build Status][build-image]][build-url]

DashPi is an easy-to-use web dashboard controller for the Raspberry Pi.  DashPi will rotate through your favorite
web dashboards, and is even configurable to handle authentication and advanced, interactive scripting to get the most
out of your data.  Simply follow the installation instructions below to get started having your Raspberry Pi rotate
through your favorite web dashboards!


## Installation Instructions

DashPi is officially supported on the Raspberry Pi 2 and 3.  Other microcontrollers, platforms, and Raspberry Pi
models *may* work, but are not formally supported by the project.


### Image Install

This is the most efficient way to install DashPi.  Use your favorite torrent application to download the image below,
and copy it to an SD Card following
[Raspberry Pi's official instructions](https://www.raspberrypi.org/documentation/installation/installing-images/).
Use `raspi-config` to expand the filesystem, as-per-normal, and edit the `~/.dashpi.yml` configuration file to suit
your needs.  Simply restart your Raspberry Pi, and your dashboards should load on startup!

(Torrent coming soon.  Please use the Web Install in the meantime.)


### Web Install

DashPi also provides an easy-install script for setting up your web dashboards on the latest version of DashPi.

**Warning:** This installation script **will** make significant changes to your Raspberry Pi configuration.  Ensure
that you are either using a fresh install of Raspbian, or that you are comfortable with the changes being made in
[this install file](https://github.com/andrewvaughan/dash-pi/blob/master/installer).  You've been warned!

1. Install the [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) image on your RaspberryPi's SD Card.

2. Connect your Raspberry Pi to the internet using either the Ethernet connection or by [setting up wifi](https://www.raspberrypi.org/documentation/configuration/wireless/).

3. SSH into the Raspberry Pi (or use the GUI's terminal) with the default credentials.  If using the GUI, you may have to switch to a terminal screen with `Ctl+Alt+F2` (you can return to the GUI with `Ctl+Alt+F7`):

   ```bash
   raspberrypi login: pi
   Password: raspberry
   ```

4. Expand your filesystem using `sudo raspi-config` and reboot when prompted.  Optionally, you can set timezone, locale, and other settings here, as well.

5. Login again and run the DashPi installer.  On a Raspberry Pi 3, this can take 10-20 minutes:

   ```bash
   bash <(curl -Ls https://andrewvaughan.io/install-dashpi)
   ```

6. [Configure your DashPi](https://github.com/andrewvaughan/dash-pi/blob/readme/README.md#configuring-dashpi) setup in the `~/.dashpi.yml` file created for you.

7. Restart your Raspberry Pi, and DashPi will launch automatically on reboot:

   ```bash
   sudo reboot
   ```

> **A friendly reminder:** don't forget to adjust the power settings on your TV or monitor to prevent it going to
> sleep! The DashPi installer will automatically configure the Raspberry Pi's display settings for you to prevent
> the Raspberry Pi from turning off the display.


### Developer Install

If you wish to contribute to DashPi, you will need to install the source from GitHub.  The requirements are packaged
using [pip](https://pypi.python.org/pypi/pip), but a Makefile is provided for your convenience:

1. Clone developer release from git (or [fork your own repository](https://github.com/andrewvaughan/dash-pi/fork))

   ```bash
   git clone https://github.com/andrewvaughan/dash-pi
   cd dash-pi
   ```

2. Install pip dependencies

   ```bash
   make dependencies
   ```

3. Test the installation (optional)

   ```bash
   make test
   ```

4. Run the Python module directly (-h for help)

   ```bash
   python -m dashpi -h
   ```


## Configuring DashPi

DashPi, by default, will look for a configuration file in your home directory at `~/.dashpi.yml`.  You can also set
a custom configuartion by running the module with the `-c` parameter.  Configuration files have the following options:

```yaml
# DashPi settings
browser : iceweasel			# Supported browsers are firefox, iceweasel, chrome, and opera
delay   : 15				# Rotation delay, in seconds

# Debugging options (command line arguments will override these options)
logfile : /tmp/dashpi.log
debug   : off
verbose : no


# Your Dashboards
dashboards:
    - url : file:///opt/dashpi/splash/index.html
    - url : https://www.google.com/
    - url : https://github.com/
```


## Upgrading DashPi

Updating is very easy - simply run the easy installer again:

```bash
bash <(curl -s https://raw.githubusercontent.com/andrewvaughan/dash-pi/master/installer)
```

This will download the latest stable version of DashPi and retain all of your configuration settings.

Don't forget to reboot when it's done!


## FAQs

### DashPi is not working, what's up?

You can do some debugging on your dashpi by enabling verbose logging in your settings file (normally located at
`~/.dashpi.yml`).  You can turn on verbose logging with the following settings:

```yml
logfile : /tmp/dashpi.log
debug   : off
verbose : no
```

When you restart DashPi (`sudo restart dashpi`), you should receive a good amount of insight into the dashboards by
looking at the log file you set.  If you believe you have discovered an unknown issue, feel free to
[open an issue](https://github.com/andrewvaughan/dash-pi/issues/new) and we will happily look into it.  Please
provided your log information when you open a ticket.


### Why do my Flash sites not load?

DashPi originally supported Chromium with flash support out of the boy, but the developers who run Chromium have
stopped providing ARM (Raspberry Pi) packages with their latest releases.  As such, we have decided to switch over to
[Iceweasel](https://wiki.debian.org/Iceweasel) (a community variant of Firefox) that does not support Flash sites.
This also helps us keep DashPi very light-weight.

Chrome is still supported with DashPi, however, with the proper Chrome Driver.  Please feel free to install Chromium
and Flash support on your own configuration!


### My question/problem is not listed here...

Feel free to [open an issue](https://github.com/andrewvaughan/dash-pi/issues/new), and we will see what we can do to
help!


## Contributing

There are many ways to contribute to DashPi!  If you have an idea, or have discovered a bug, please
[open an issue](https://github.com/andrewvaughan/dash-pi/issues) so it can be addressed.

If you are interested in contributing to the project through design or development, please read our
[Contribution Guidelines](https://github.com/andrewvaughan/dash-pi/blob/master/CONTRIBUTING.md).


## Release Policy

Releases of DashPi follow [Semantic Versioning](http://semver.org/) standards in a `MAJOR.MINOR.PATCH` versioning
scheme of the following format:

* `MAJOR` - modified when major, incompatible changes are made to the application,
* `MINOR` - modified when functionality is added in a backwards-compatible manner, and
* `PATCH` - patches to existing functionality, such as documentation and bug fixes.


## License

For more information, see the [Project License][license-url].

```
The MIT License (MIT)

Copyright (c) 2016 Andrew Vaughan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```



[version-image]:  http://img.shields.io/badge/release-0.0.0-blue.svg?style=flat
[version-url]:    https://github.com/andrewvaughan/dash-pi/releases
[license-image]:  http://img.shields.io/badge/license-MIT-blue.svg?style=flat
[license-url]:    https://github.com/andrewvaughan/dash-pi/blob/master/LICENSE
[build-image]:    https://travis-ci.org/andrewvaughan/dash-pi.svg?branch=master
[build-url]:      https://travis-ci.org/andrewvaughan/dash-pi
