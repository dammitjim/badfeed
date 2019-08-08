FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY Pipfile /code/
COPY Pipfile.lock /code/

RUN pip install pipenv
RUN pipenv install --dev --system --ignore-pipfile

COPY . /code/
