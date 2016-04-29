# DashPi


"""DashPi the web dashboard controller for Raspberry Pi"""


import subprocess
import sys

from selenium import webdriver


def main():
    """Launches DashPi"""
    
    config = dict()
    
    config['browser'] = "firefox"
    
    try:
        process = subprocess.check_output(["pgrep", config['browser']])
    
        if process != "":
            print "The \"%s\" browser is already running, please close and re-run DashPi." % config['browser']
            return
    except subprocess.CalledProcessError:
        pass
    
    print "Launching %s" % config['browser']
    
    browser = webdriver.Firefox()
    browser.get('https://andrewvaughan.io/')


if __name__ == "__main__":
    sys.exit(main())
