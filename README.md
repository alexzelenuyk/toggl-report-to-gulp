[![CircleCI](https://circleci.com/gh/alexzelenuyk/toggl-report-to-gulp.svg?style=svg&circle-token=e12e1736696edaf7eeb104635d933822e1648cfc)](https://circleci.com/gh/alexzelenuyk/toggl-report-to-gulp)

# Script to generate pdf report for GULP ([Leistungsnachweis](https://www.gulp.de/gutschriftverfahren/Merkblatt-Leistungsnachweis.pdf))

_Motivation_: Those, who work together with [Gulp](https://www.gulp.de/), need to provide report at the end of the month with performance records.
In case, [Toggl](https://toggl.com/) tracker is used, the report generation can be automated using current script.

## Local install

## Install Pipenv

Project use [Pipenv](https://docs.pipenv.org/en/latest/) as package manager.

```bash
> pip install pipenv
```

## Create virtual environment

```bash
> pipenv --python 3.8
```

## Install dependencies

```bash
> pipenv install
```

# Generate detailed report

## Local run

```bash

> ./cli.py \
  --api-key {KEY}  \
  --workspace Test \
  --year 5 \
  --month-number 5 \
  --name "Max Mustermann" \
  --project-number Test \
  --client-name "Muster GmbH" \
  --order-no 123456

```

## Run with docker

```bash

> make run \
    api_key={KEY} \
    workspace=Test \
    month_number=5 \
    year=5 \
    name="Max Mustermann" \
    project_number="Test" \
    client_name="Muster GmbH" \
    order_no=123456

```

# Result

![report sample](https://github.com/alexzelenuyk/toggl-report-to-gulp/blob/master/doc/report_sample.png "Report sample")

# Development

## Lint

```bash
> make lint

```

## Tests

```bash
> make test

```
