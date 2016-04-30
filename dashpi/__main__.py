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


"""DashPi the web dashboard controller for Raspberry Pi"""


import logging
import os
import subprocess
import sys
import traceback

import argparse
import selenium

from selenium import webdriver
from yaml import load as loadconfig


def main(args):
    """Launches DashPi"""
    
    logger = logging.getLogger('DashPi')
    
    # Load the user's configuration file
    logger.debug('Loading configuration from "%s"', args.config)
    
    try:
        with open(args.config, 'r') as yml:
            config = loadconfig(yml)
        
    except IOError:
        raise SystemExit('The configuration file "%s" could not be found' % args.config)
    
    logger.debug('Loaded.')
    
    
    # Ensure the user has set a browser
    if not config or not config['browser'] or config['browser'] not in ['firefox', 'iceweasel', 'chrome', 'opera']:
        raise SystemExit('Configuration option "browser" must be one of: firefox, iceweasel, chrome, ie, opera')
    
    
    logger.debug('Browser set to "%s"', config['browser'])
    
    
    # Check if the browser is already running
    logger.debug('Checking if browser currently running...')
    try:
        process = subprocess.check_output(["pgrep", config['browser']])
    
        if process != "":
            raise SystemExit(
                "The \"%s\" browser is already running, please close and re-run DashPi." % config['browser']
            )
        
    except subprocess.CalledProcessError:
        logger.debug('Browser not found.')
    
    
    # Launch the browser
    logger.info("Launching %s...", config['browser'])
    
    if config['browser'] == 'chrome':
        browser = webdriver.Chrome()
        
    elif config['browser'] == 'opera':
        browser = webdriver.Opera()     # pylint: disable=redefined-variable-type
        
    else:
        browser = webdriver.Firefox()   # pylint: disable=redefined-variable-type
    
    
    # Load a test URL
    logger.debug("Loading URL int browser")
    
    browser.get('https://andrewvaughan.io/')



if __name__ == "__main__":
    
    # Setup runtime arguments
    PARSER = argparse.ArgumentParser(prog="dashpi", description='DashPi: the Rapsberry Pi web dashboard controller')
    
    PARSER.add_argument('-c', '--config', default='~/dashpi.yml',
                        help="configuration file (default: ~/dashpi.yml)")
    
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

        ARGS.setFormatter(
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
        main(ARGS)
        
    except SystemExit, err:
        LOGGER.error(str(err))
        sys.exit(1)
    
    except selenium.common.exceptions.WebDriverException, err:
        LOGGER.error("DashPi could not connect to the web browser.")
        LOGGER.error(str(err))
        sys.exit(2)
