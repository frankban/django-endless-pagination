# Django Endless Pagination Makefile.

ifdef PYTHON3
	PYTHON = python3
	VENV = .venv3
else
	PYTHON = python2
	VENV = .venv
endif

PYFILES = `find ./endless_pagination -name "*.py"`
WITH_VENV = ./tests/with_venv.sh $(VENV)

all:
	@echo -e 'Django Endless Pagination - list of make targets:\n'
	@echo 'make develop - Set up development and testing environment'
	@echo 'make test - Run tests'
	@echo 'make pep8 - Run pep8'
	@echo 'make lint - Run linter'
	@echo 'make check - Run tests, pep8 and lint'
	@echo 'make testall - Run tests including integration ones'
	@echo 'make doc - Build Sphinx documentation'
	@echo 'make opendoc - Build Sphinx documentation and open it in browser'
	@echo 'make source - Create source package'
	@echo 'make install - Install on local system'
	@echo 'make shell - Enter Django interactive interpreter'
	@echo 'make server - Run Django development server'
	@echo 'make clean - Get rid of bytecode files, build dirs, dist files'
	@echo 'make cleanall - Clean and also get rid of the virtualenv'
	@echo -e '\nDefine the env var PYTHON3 to work using Python 3.'
	@echo 'E.g. to create a Python 3 development environment:'
	@echo '  - make develop PYTHON3=yes'

doc:
	@$(WITH_VENV) make -C doc html

clean:
	$(PYTHON) setup.py clean
	rm -rfv .coverage build/ dist/ doc/_build MANIFEST
	find . -name '*.pyc' -delete

cleanall: clean
	rm -rfv .venv .venv3

check: test lint pep8

develop:
	@$(PYTHON) ./tests/develop.py

install:
	python setup.py install

lint:
	@pocketlint $(PYFILES)

opendoc: doc
	@firefox ./doc/_build/html/index.html

pep8:
	@$(WITH_VENV) pep8 --show-source $(PYFILES)

server:
	@$(WITH_VENV) python ./tests/manage.py runserver 0.0.0.0:8000

shell:
	@$(WITH_VENV) python ./tests/manage.py shell

source:
	$(PYTHON) setup.py sdist

test:
	@$(WITH_VENV) python ./tests/manage.py test

testall:
	@USE_SELENIUM=1 $(WITH_VENV) python ./tests/manage.py test

.PHONY: all doc clean cleanall check develop install lint opendoc pep8 server \
	shell source test testall
