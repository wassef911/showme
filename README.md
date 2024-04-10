# showme

This is a dummy project part of march side sprint.

![demo_resource_visualizer](https://raw.githubusercontent.com/wassef911/showme/master/demo_resource_visualizer.png)

## Development

To run the project locally use this set of commands:

```bash
python3 -v venv venv
source venv/bin/activate
python -m pip install install -r requirements.txt # just for type hints
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## Project structure

```bash
showme
├── conftest.py
├── db
│   ├── base.py
│   ├── dependencies.py
│   ├── meta.py
│   ├── migrations
│   ├── models
│   └── utils.py
├── gunicorn_runner.py
├── log.py
├── services
│   ├── blob
│   ├── image
│   ├── kafka
│   └── redis
├── settings.py
├── static
├── tests
├── tkq.py
└── web
    ├── api
    │   ├── country
    │   ├── kafka
    │   ├── monitoring
    │   ├── router.py
    │   └── users
    ├── application.py
    ├── dependencies.py
    └── lifetime.py
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "SHOWME\_" prefix.

For example if you see in your "showme/settings.py" a variable named like
`random_parameter`, you should provide the "SHOWME_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `showme.settings.Settings.Config`.

An example of .env file:

```bash
SHOWME_RELOAD="True"
SHOWME_PORT="8000"
SHOWME_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

You can read more about pre-commit here: https://pre-commit.com/

## Migrations

If you want to migrate your database, you should run following commands:

```bash
# To run all migrations until the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```
