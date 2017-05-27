.PHONY: bootstrap clean lint test

lint:
	@flake8 tinyenv

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@pip install -r requirements.txt
	@python setup.py develop

test: lint
	py.test --cov-report term-missing --cov=tinyenv tests/
