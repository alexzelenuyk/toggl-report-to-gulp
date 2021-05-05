# Development

lint:
	flake8

test: clean
	pytest

clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# Run
build:
	docker build -t toggl-report-to-gulp .

run: build
	docker run --rm -v ${CURDIR}:/app toggl-report-to-gulp \
	--api-key $(api_key) \
	--workspace "$(workspace)" \
	--month-number $(month_number) \
	--year $(year) \
	--name "$(name)" \
	--project-number "$(project_number)"  \
	--client-name "$(client_name)"  \
	--order-no $(order_no)

verify-package: setup-package
	twine check dist/*

setup-package:
	python setup.py sdist bdist_wheel

publish: verify-package
	twine upload  dist/*

.PHONY: lint test build run