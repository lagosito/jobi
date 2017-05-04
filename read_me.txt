### In order of Execution [run from project source in environment]
### Some commands will change for production while some will be obsolete


## Database migrations
$ python manage.py makemigrations
$ python manage.py migrate


## Create Superuser
$ python manage.py createsuperuser


## Start Celery and its Beat Scheduler
$ celery -A src worker -B -l info


## Initialize ElasticSearch
$ python manage.py initialize_site


## Start python Server
$ python manage.py runserver


## To update ElasticSearch [capable on runtime]
$ python manage.py force_update_es


Run the command python -m nltk.downloader all. To ensure central installation, run the command sudo python -m nltk.downloader -d /usr/local/share/nltk_data all.