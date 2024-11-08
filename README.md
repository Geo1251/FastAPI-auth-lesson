# Du Rove's Wall API
REST API service for a social wall with posts.

## Requirements

```console
python 3.8+
```

## First run

```console
$ pip install -r requirements.txt
$ python migrate.py
$ python -m duroveswall
```

## Run tests

```console
$ python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
```

## Run linter

```console
$ pylint duroveswall
```
