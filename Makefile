.PHONY: all dependencies test clean


all: dependencies


dependencies:
	#sudo apt-get install python-pip iceweasel xvfb
	sudo -H pip install --upgrade -r requirements.txt


test:
	@echo "LINTING ***********************************************************************"
	@pylint dashpi --rcfile=.pylintrc
	@find ./dashpi/tests/ -name *.py | xargs pylint --rcfile=.pylintrc
	
	@echo "UNIT TESTING ******************************************************************"


clean:
	@-find . -type f -name '*.pyc' -delete ||: > /dev/null 2>&1
	@-rm -rf .coverage coverage.xml htmlcov ||: > /dev/null 2>&1
