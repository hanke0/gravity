.PHONY: build
build:
	@python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	@find . -name *.egg-info -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-all
clean-all: clean
	@rm -rf dist build

.PHONY: install
install:
	@pip install .

.PHONY: upload
upload:
	twine upload dist/* --skip-existing -r $(r)
