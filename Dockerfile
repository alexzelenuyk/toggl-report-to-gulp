FROM python:3.7

RUN apt-get update \
 && apt-get install -y locales locales-all

ENV LC_ALL de_DE.UTF-8
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE.UTF-8

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "/"]

RUN pipenv install --system --deploy

COPY . /app

WORKDIR /app

ENTRYPOINT ["./cli.py"]