# bmd-micro

A micro service that manages "Users" and "Falling Rocks"
Interaction  is made available through a restful service API.
Data is stored in a postgres database.

Steps to run locally:
- install docker
- 'make build'
- 'make initDB'
- 'make run'
- 'make test'
- ./curl_local.sh (run some curls against the api)


The app is currently deployed to production at https://bmd-micro.herokuapp.com
Give it a spin with
./curl_production.sh
./curl_production_rocks.sh

![](bmd-micro-demo.gif)

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

## USERS
This endpoint was added November 2019. As part of engineering take home No changes to that part of the application made since

### Completed Tasks
- A User rest Resource that allows clients to create, read, update, delete a user or list a bunch of users.
- use a database to keep track of users
- logging and unit tests
- The user JSON id, first name, last name, zip code, and email address.
- structured logging
- Generate a code coverage report
- Log Metrics (but currently not integrated to a monitoring system)

![](test_and_codecoverage.gif)

### not completed Tasks
- show metrics and logs in a monitoring system such as datadog

### things I like to add
* show metrics and logs in a monitoring system such as datadog
* code refactoring
    * Tests, currently a lot of repetition
    * User Model, check valid zipCode and email
    * generally "DRY"ing the code
* add authentication
* add fancy documentation with SWAGGGER
* Deploy to AWS instead of heroku
* Provision production infrastructure with terraform

## Falling Rocks

Rocks are falling out of the sky! They fall in columns, and collect in stacks on the ground or on a table. Folks need to know how the rocks will land, so they can get to safety.

### Completed Task
* HTTP route for GET and INSERT
* "gravity" processing (see models.rockworld.falling_rocks)
* metrics
* tests & logs

### not completed task
* update route