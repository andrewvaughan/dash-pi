# DashPi

[![Version][version-image]][version-url]
[![License][license-image]][license-url]
[![Build Status][build-image]][build-url]

DashPi is an easy-to-use dashboard controller for the Raspberry Pi.  Simply follow the [Easy Install](#Easy-Install)
instructions below to get started and have your Raspberry Pi rotate through your favorite web dashboards!


## Installation Instructions

DashPi is officially supported on the Raspberry Pi 2 and 3.  Other linux systems, microcontrollers, and other
Raspberry Pi models may work, but are not formally supported by this organization.


### Image Install

This is the most efficient way to install DashPi.  Simply download the image below and image it to a SD Card.  Expand
the filesystem as per normal, with `raspi-config`, and configure the `~/.dashpi.yml` file to suit your needs.

(Torrent coming soon)


### Web Install

DashPi provides an easy-install script for setting up your Dashboards on the latest version of DashPi:

1. Install the [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) image on your RaspberryPi's SD Card.

2. Connect the Raspberry Pi to the internet using either the Ethernet connection or by [setting up wifi](https://www.raspberrypi.org/documentation/configuration/wireless/)

3. SSH into the Raspberry Pi (or use the GUI's terminal) with the default credentials:
   
   ```bash
   raspberrypi login: pi
   Password: raspberry
   ```

4. Expand your filesystem using `sudo raspi-config` and reboot when prompted.  Optionally, you can set timezone, locale, and other settings here, as well.

5. Login again and run the DashPi installer.  On a Raspberry Pi 3, this can take 10-20 minutes:
   
   ```bash
   bash <(curl -s https://raw.githubusercontent.com/andrewvaughan/dash-pi/master/installer)
   ```

6. [#Configuring-DashPi](Configure your DashPi) setup in the `~/.dashpi.yml` file created for you.

7. Restart your RaspberryPi, and DashPi will launch automatically:
   
   ```bash
   sudo reboot
   ```

> **A friendly reminder:** don't forget to adjust the power settings on your TV or monitor to prevent it going to
> sleep! The DashPi installer will automatically configure the Raspberry Pi's display settings for you to prevent
> the Raspberry Pi from turning off the display.


### Developer Install

If you wish to contribute to DashPi, you will need to install the source from GitHub.  The requirements are packaged
using pip, but a Makefile is provided for your convenience:

1. Clone developer release from git
   
   ```bash
   git clone https://github.com/andrewvaughan/dash-pi
   cd dash-pi
   ```

2. Install [pip](https://pypi.python.org/pypi/pip) dependencies
   
   ```bash
   make dependencies
   ```

3. Test installation
   
   ```bash
   make test
   ```

4. Run the Python module (-h for help)
   
   ```bash
   python -m dashpi -h
   ```


## Configuring DashPi

Coming soon.


## Upgrading DashPi

Updating is very easy - simply run the easy installer again:

```bash
bash <(curl -s https://raw.githubusercontent.com/andrewvaughan/dash-pi/master/installer)
```

This will download the latest stable version of DashPi and retain all of your configuration settings.

Don't forget to reboot when it's done!


## FAQs

TBD


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

Please see the [Project License][license-url].



[version-image]:  http://img.shields.io/badge/release-0.0.0-blue.svg?style=flat
[version-url]:    https://github.com/andrewvaughan/dash-pi/releases
[license-image]:  http://img.shields.io/badge/license-MIT-blue.svg?style=flat
[license-url]:    https://github.com/andrewvaughan/dash-pi/blob/master/LICENSE
[build-image]:    https://travis-ci.org/andrewvaughan/dash-pi.svg?branch=master
[build-url]:      https://travis-ci.org/andrewvaughan/dash-pi
