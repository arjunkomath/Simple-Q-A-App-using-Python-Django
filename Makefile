.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test: ## run tests quickly with the default Python
	python runtests.py tests

coverage: ## check code coverage quickly with the default Python
	coverage run --source django-qa runtests.py tests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django-qa.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django-qa
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean ## package
	python setup.py sdist
	ls -l dist

history: ## Generate the history report from the git log comments records
	rm HISTORY.rst
	printf '%s\n' '.. :changelog:' '' 'History' '-------' >> HISTORY.rst
	git log --no-merges --pretty=format:'Commit `#%h <https://github.com/swappsco/django-qa/commit/%H>`_ %n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%n%n* %cd - %s%n' >> HISTORY.rst
