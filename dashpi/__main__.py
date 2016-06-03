# DashPi
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Andrew Vaughan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#pylint: disable=too-many-branches,too-many-statements


"""DashPi the web dashboard controller for Raspberry Pi"""


import logging
import os
import subprocess
import sys
import time
import traceback

import argparse
import selenium

from selenium import webdriver
from yaml import load as loadconfig


def main(args):
    """Launches DashPi"""

    logger = logging.getLogger('DashPi')


    # Set display
    #logger.debug('Setting display to :0.0')
    #os.environ["DISPLAY"] = ":0.0"


    # Load the user's configuration file
    logger.debug('Loading configuration from "%s"', args.config)

    try:
        with open(args.config, 'r') as yml:
            config = loadconfig(yml)

    except IOError:
        logger.error('The configuration file "%s" could not be found', args.config)
        return False


    # See if the configuration file has debugging set (command line overrides this)
    if (ARGS.verbose is None or ARGS.verbose <= 0) and 'debug' in config and config['debug'] is True:
        if 'verbose' in config and config['verbose'] is True:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)


    # See if a log file is set (command line overrides this)
    if ARGS.log is None and 'logfile' in config:
        log_file = logging.FileHandler(config['logfile'])

        log_file.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s] %(name)-12s :: %(levelname)-8s : %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S'
            )
        )

        logging.getLogger().addHandler(log_file)


    logger.debug('Configuration file loaded.')


    # Ensure the user has set a browser
    if not config or 'browser' not in config or config['browser'] not in ['firefox', 'iceweasel', 'chrome', 'opera']:
        logger.error('Configuration option "browser" must be one of: firefox, iceweasel, chrome, opera')
        return False


    logger.debug('Browser set to "%s"', config['browser'])


    # Get our delay
    if 'delay' not in config:
        logger.warn('No delay configured, defaulting to 15 seconds')
        config['delay'] = 15

    if not isinstance(config['delay'], (int, long)) or config['delay'] <= 0:
        logger.warn('Delay is not a whole, positive number, defaulting to 15 seconds')
        config['delay'] = 15


    # Ensure we have some dashboards and URLs
    if 'dashboards' not in config or not isinstance(config['dashboards'], list) or len(config['dashboards']) <= 0:
        logger.error('No dashboards defined')
        return False


    # Check if the browser is already running
    logger.debug('Checking if browser currently running...')
    try:
        process = subprocess.check_output(["pgrep", config['browser']])

        if process != "":
            logger.error("The \"%s\" browser is already running, please close and re-run DashPi.", config['browser'])
            return False

    except subprocess.CalledProcessError:
        logger.debug('Browser not found.')


    # Launch the browser
    logger.info("Launching %s...", config['browser'])

    if config['browser'] == 'chrome':
        browser = webdriver.Chrome()    # pylint: disable=redefined-variable-type

    elif config['browser'] == 'opera':
        browser = webdriver.Opera()     # pylint: disable=redefined-variable-type

    else:
        logger.debug("Creating Firefox profile")
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.sessionstore.resume_from_crash", False)
        profile.set_preference("capability.policy.default.Window.open", "noAccess")
        profile.set_preference("capability.policy.default.Window.alert", "noAccess")
        profile.set_preference("capability.policy.default.Window.confirm", "noAccess")
        profile.set_preference("capability.policy.default.Window.prompt", "noAccess")

        logger.debug("Launching Firefox with WebDriver")
        browser = webdriver.Firefox(firefox_profile=profile, timeout=60) # pylint: disable=redefined-variable-type


    # Rotate through URLS
    counter = 0
    total = len(config['dashboards'])

    logger.info("Beginning rotation of %d dashboards at %d second intervals", total, config['delay'])

    while True:
        dashboard = config['dashboards'][counter % total]

        if 'url' not in dashboard:
            logger.warning('URL missing from dashboard #%d, skipping', (counter % total) + 1)
            counter += 1
            continue

        logger.info("Loading dashboard #%d: %s", (counter % total) + 1, dashboard['url'])

        browser.get(dashboard['url'])

        counter += 1
        time.sleep(config['delay'])


    # Exit
    logger.debug('Exiting')
    return True



if __name__ == "__main__":

    # Setup runtime arguments
    PARSER = argparse.ArgumentParser(prog="dashpi", description='DashPi: the Rapsberry Pi web dashboard controller')

    PARSER.add_argument('-c', '--config', default=os.path.expanduser('~') + '/.dashpi.yml',
                        help="configuration file (default: ~/.dashpi.yml)")

    PARSER.add_argument('-q', '--quiet', action='store_true',
                        help='prevents output to stdout')

    PARSER.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level for logging (-vv for max verbosity)')

    PARSER.add_argument('-l', '--log',
                        help='the log file to write to')

    ARGS = PARSER.parse_args()


    # Setup the logger
    LOGGER = logging.getLogger()

    LOGGER.setLevel(logging.WARNING)

    if hasattr(ARGS, 'verbose'):
        if ARGS.verbose == 1:
            LOGGER.setLevel(logging.INFO)

        elif ARGS.verbose == 2:
            LOGGER.setLevel(logging.DEBUG)

        elif ARGS.verbose > 2:
            LOGGER.setLevel(1)


    # Setup console logging
    SH_CONSOLE = logging.StreamHandler(sys.stdout)

    SH_CONSOLE.setFormatter(
        logging.Formatter(
            fmt='%(name)-12s :: %(levelname)-8s : %(message)s'
        )
    )

    if ARGS.quiet:
        sys.stdout = os.devnull
        SH_CONSOLE.setLevel(9999)

    LOGGER.addHandler(SH_CONSOLE)


    # Setup file logging
    if ARGS.log != None:
        SH_FILE = logging.FileHandler(ARGS.log)

        SH_FILE.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s] %(name)-12s :: %(levelname)-8s : %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S'
            )
        )

        LOGGER.addHandler(SH_FILE)


    # Send all exceptions through the logger
    def handle_exception(ex_cls, ex, trace):
        """Catches all errors and sends them through the logger"""

        LOGGER.critical("EXCEPTION")
        LOGGER.critical(''.join(traceback.format_tb(trace)))
        LOGGER.critical('%s: %s', ex_cls, ex)

    sys.excepthook = handle_exception


    # Launch and exit with the proper code
    try:
        if not main(ARGS):
            sys.exit(1)

    except selenium.common.exceptions.WebDriverException, err:
        LOGGER.error("DashPi could not connect to the web browser.")
        LOGGER.error(str(err))
        sys.exit(2)
