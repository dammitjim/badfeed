# Project BADFEED

Badfeed is the codename for an experimental RSS reader with a focus on
reduction of noise. The goal is to surface content that may otherwise be missed
due to the publishing velocity of noisier feeds, while also providing the tools
to manage the large amount of clutter.

In short, there are publications where 1 in 10 stories are worth reading, dealing
with those other 9 is a pain in the ass.

The project is in early stages.

## Dependencies

* Python 3.6
* Postgresql
* Redis

## Installation for development

```bash
pipenv install --dev
pre-commit install --install-hooks
```

### Running the server

The raw way

```bash
python manage.py runserver
```

The docker way

```bash
docker-compose up
```

### Running the workers

This step is not needed if you are using docker compose.

```bash
python manage.py rqworker default
```

### Queueing work

```bash
python manage.py queue_feeds
```
