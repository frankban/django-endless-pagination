pyfiles = `find ./endless_pagination -name "*.py"`

clean:
	rm -rfv .venv

check: test lint pep8

develop:
	@python ./tests/develop.py

lint:
	@pocketlint $(pyfiles)

pep8:
	@./tests/with_venv.sh pep8 --show-source $(pyfiles)

test:
	@./tests/with_venv.sh python ./tests/runtests.py

.PHONY: clean check develop lint pep8 test
