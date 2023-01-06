FROM python:3.10
ENV POETRY_VERSION=1.3.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/local/src/crawler
COPY . /usr/local/src/crawler

RUN apt-get update
RUN apt-get -y install default-jdk
RUN poetry install --no-interaction --no-ansi

CMD poetry run scrapy list | xargs -n 1 poetry run scrapy crawl
