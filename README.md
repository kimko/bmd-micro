# bmd-micro
A micro service that manages users. Interaction with users
is made available through a restful service API.
Data is stored in a postgres database.

Steps to run locally:
- install docker
- 'make build'
- 'make run'
- 'make tests'
- ./curl_local.sh (run some curls against the api)

The app is currently deployed to production at https://bmd-micro.herokuapp.com
Give it a spin with
./curl_production.sh

![](bmd-micro-demo.gif)

## Notes for local development without container
install postgres:
brew install postgresql

run postgres:
brew services start postgresql

check if server is listening (postgres 9.3 or higher):
pg_isready
/tmp:5432 - accepting connections

psql --host localhost --dbname postgre

postgres=# CREATE DATABASE bmdmicro_dev;
postgres=# CREATE DATABASE bmdmicro_test;
postgres=# CREATE DATABASE bmdmicro_prod;
postgres=# create user postgres  with encrypted password 'postgres';
postgres=# grant all privileges on database bmdmicro_dev to postgres;
postgres=# grant all privileges on database bmdmicro_test to postgres;
postgres=# grant all privileges on database bmdmicro_prod to postgres;

add environment vars: (IE: ~/.virtualenvs/bmd-micro/bin/postactivate)
export FLASK_ENV=development
export APP_SETTINGS=project.config.DevelopmentConfig
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bmdmicro_dev
export DATABASE_TEST_URL=postgresql://postgres:postgres@localhost:5432/bmdmicro_dev

create tables
python manage.py recreate_db

run the thing:
python manage.py run -h 0.0.0.0

## Technologies
- Core:
    - Python3.7
    - flask restful
    - docker (api on 3.7.4-alpine)
- Dev/Test:
    - another docker (db on postgres:11.4-alpine)
    - pytest, flake8, black and isort
    - code coverage
- Production:
    - Heroku

## Completed Tasks
- A User rest Resource that allows clients to create, read, update, delete a user or list a bunch of users.
- use a database to keep track of users
- logging and unit tests
- The user JSON id, first name, last name, zip code, and email address.
- structured logging
- Generate a code coverage report
- Log Metrics (but currently not integrated to a monitoring system)

![](test_and_codecoverage.gif)

## not completed Tasks
- show metrics and logs in a monitoring system such as datadog

## things I like to add
* show metrics and logs in a monitoring system such as datadog
* code refactoring
    * Tests, currently a lot of repetition
    * User Model, check valid zipCode and email
    * generally "DRY"ing the code
* add authentication
* add fancy documentation with SWAGGGER
* Deploy to AWS instead of heroku
* Provision production infrastructure with terraform
