# Django Endless Pagination Makefile.

# Define these variables based on the system Python versions.
PYTHON2 = python
PYTHON3 = python3

VENV2 = .venv
VENV3 = .venv3

DEVELOP = ./tests/develop.py
LINTER = pocketlint
MANAGE = python ./tests/manage.py

ifdef PY3
	PYTHON = $(PYTHON3)
	VENV = $(VENV3)
else
	PYTHON = $(PYTHON2)
	VENV = $(VENV2)
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
	@echo 'make venv - Set up development environment if it does not exist'
	@echo -e '\nDefine the env var PY3 to work using Python 3.'
	@echo 'E.g. to create a Python 3 development environment:'
	@echo '  - make develop PY3=yes'

doc: venv
	@$(WITH_VENV) make -C doc html

clean:
	$(PYTHON) setup.py clean
	rm -rfv .coverage build/ dist/ doc/_build MANIFEST
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

cleanall: clean
	rm -rfv $(VENV2) $(VENV3)

check: test lint pep8

develop:
	@$(PYTHON) $(DEVELOP)

install:
	python setup.py install

lint:
	@$(LINTER) $(PYFILES)

opendoc: doc
	@firefox ./doc/_build/html/index.html

pep8: venv
	@$(WITH_VENV) pep8 --show-source $(PYFILES)

release: clean
	python setup.py register sdist upload

server: venv
	@$(WITH_VENV) $(MANAGE) runserver 0.0.0.0:8000

shell: venv
	@$(WITH_VENV) $(MANAGE) shell

source:
	$(PYTHON) setup.py sdist

test: venv
	@$(WITH_VENV) $(MANAGE) test

testall: venv
	@USE_SELENIUM=1 $(WITH_VENV) $(MANAGE) test

venv:
	@[ ! -d $(VENV) ] && $(PYTHON) $(DEVELOP) || true

.PHONY: all doc clean cleanall check develop install lint opendoc pep8 \
	release server shell source test testall venv
