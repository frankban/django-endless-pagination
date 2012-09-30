pyfiles = `find ./endless_pagination -name "*.py"`

clean:
	rm -rfv .coverage .venv

check: test lint pep8

develop:
	@python ./tests/develop.py

lint:
	@pocketlint $(pyfiles)

pep8:
	@./tests/with_venv.sh pep8 --show-source $(pyfiles)

shell:
	@./tests/with_venv.sh python ./tests/manage.py shell

test:
	@./tests/with_venv.sh python ./tests/manage.py test

.PHONY: clean check develop lint pep8 shell test
