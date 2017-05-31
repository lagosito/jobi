#### In order of Execution [run from project source in environment]

## Pre-requisites
# ElasticSearch Installation and running
# RabbitMQ Installation, setup and running
# PostgreSQL Installation, setup and running


## External dependencies

# Used by polyglot for mining
$ sudo apt-get install python-numpy libicu-dev


## Get all dependencies (in an existing Environment)
$ pip install -r requirements.txt


## Database migrations
$ python manage.py makemigrations
$ python manage.py migrate


## Create Superuser
$ python manage.py createsuperuser


## Initialize ElasticSearch and NLP toolkit
## [--download] tag will fetch all the needed NLP libraries. Important for the first time.
$ python manage.py initialize_site --download


## Start Celery and its Beat Scheduler
$ celery -A src worker -B -l info


## Start python Server
$ python manage.py runserver


#### Following commands aren't setup related but may be needed in future


## To update ElasticSearch mappings
## WARNING: It won't handle deletions in ES mappings
## Capable on runtime
$ python manage.py es_force_migrate


## To instantiate a mining process manually for a particular source
## [source_name] is essential as stored in the database
## Capable on runtime
$ python manage.py force_mine_source [source_name]


## To instantiate a mining process manually for all stored sources
## Capable on runtime
$ python manage.py force_mine_source_all

