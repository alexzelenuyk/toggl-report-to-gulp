# Development

lint:
	flake8

test: clean
	pytest

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

.PHONY: lint test