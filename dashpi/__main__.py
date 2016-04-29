# DashPi


"""DashPi the web dashboard controller for Raspberry Pi"""


import subprocess
import sys

import argparse
import selenium

from selenium import webdriver
from yaml import load as loadconfig


def main(args):
    """Launches DashPi"""
    
    # Load the user's configuration file
    try:
        with open(args.config, 'r') as yml:
            config = loadconfig(yml)
        
    except IOError:
        raise SystemExit('The configuration file "%s" could not be found' % args.config)
    
    
    # Ensure the user has set a browser
    if not config or not config['browser'] or config['browser'] not in ['firefox', 'iceweasel', 'chrome', 'opera']:
        raise SystemExit('Configuration option "browser" must be one of: firefox, iceweasel, chrome, ie, opera')
    
    
    # Check if the browser is already running
    try:
        process = subprocess.check_output(["pgrep", config['browser']])
    
        if process != "":
            raise SystemExit(
                "The \"%s\" browser is already running, please close and re-run DashPi." % config['browser']
            )
        
    except subprocess.CalledProcessError:
        pass
    
    
    # Launch the browser
    print "Launching %s..." % config['browser']
    
    if config['browser'] == 'chrome':
        browser = webdriver.Chrome()
        
    elif config['browser'] == 'opera':
        browser = webdriver.Opera()     # pylint: disable=redefined-variable-type
        
    else:
        browser = webdriver.Firefox()   # pylint: disable=redefined-variable-type
    
    
    # Load a test URL
    browser.get('https://andrewvaughan.io/')



if __name__ == "__main__":
    
    # Setup runtime arguments
    PARSER = argparse.ArgumentParser(prog="dashpi", description='DashPi: the Rapsberry Pi web dashboard controller')
    
    PARSER.add_argument('-c', '--config', default='~/dashpi.yml',
                        help="configuration file (default: ~/dashpi.yml)")
    
    
    # Launch and exit with the proper code
    try:
        main(PARSER.parse_args())
        
    except SystemExit, err:
        print "Error: %s" % str(err)
        sys.exit(1)
    
    except selenium.common.exceptions.WebDriverException, err:
        print "DashPi could not connect to the web browser:"
        print str(err)
        sys.exit(2)
