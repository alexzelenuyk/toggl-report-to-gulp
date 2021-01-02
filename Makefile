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

.PHONY: lint test build run