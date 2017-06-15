SHELL=/bin/bash

lint:
	./setup.py flake8
	flake8 scripts/*

test: lint
	python ./test/test.py -v

init_docs:
	cd docs; sphinx-quickstart

docs:
	$(MAKE) -C docs html

install:
	-rm -rf dist
	python setup.py bdist_wheel
	pip install --upgrade dist/*.whl

.PHONY: test release docs

include common.mk
