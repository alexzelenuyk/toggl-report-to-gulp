[![CircleCI](https://circleci.com/gh/alexzelenuyk/toggl-report-to-gulp.svg?style=svg&circle-token=e12e1736696edaf7eeb104635d933822e1648cfc)](https://circleci.com/gh/alexzelenuyk/toggl-report-to-gulp)

# Script to generate pdf report for GULP ([Leistungsnachweis](https://www.gulp.de/gutschriftverfahren/Merkblatt-Leistungsnachweis.pdf))

*Motivation*: Those, who work together with [Gulp](https://www.gulp.de/), need to provide report at the end of the month with performance records.
In case, [Toggl](https://toggl.com/) tracker is used, the report generation can be automated using current script.


## Install

## Install Pipenv

Project use [Pipenv](https://docs.pipenv.org/en/latest/) as package manager.

```bash
> pip install pipenv
```

## Create virtual environment

```bash
> pipenv --python 3.7
```

## Install dependencies

```bash
> pipenv install
```

# Generate detailed report

```bash

> ./cli.py \
  --api-key {KEY}  \
  --workspace Test \
  --month-number 5 \
  --name "Max Mustermann" \
  --project-number Test \
  --client-name "Muster GmbH" \
  --order-no 123456

```


# Development

## Lint

```bash
> make lint

```

## Tests

## CI
