clean:
	rm -rfv .venv

check: test lint pep8

develop:
	@python ./tools/install_venv.py

lint:
	@pocketlint `find ./endless_pagination -name "*.py"`

pep8:
	@pep8 --show-source `find ./endless_pagination -name "*.py"`

test:
	@./tools/with_venv.sh python ./tests/runtests.py

.PHONY: clean check develop lint pep8 test
