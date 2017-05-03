from django.conf import settings

# Celery settings
# http://celery.readthedocs.org/en/latest/index.html
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
broker_url = settings.CELERY_BROKER_URL
enable_utc = True
timezone = settings.TIME_ZONE
result_backend = 'django-db'
accept_content = ['json', 'pickle']
task_serializer = "json"
result_serializer = "json"
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
beat_schedule = {
    'update-scrappers-every-hour': {
        'task': 'scrapper_handler',
        'schedule': settings.RMQ_REFRESH_RATE,
    },
}
broker_heartbeat = 10
# broker_heartbeat_checkrate = 2  # default
# broker_pool_limit = 10  # default
result_expires = 0
task_track_started = True
worker_send_task_events = True
task_send_sent_event = True
worker_disable_rate_limits = True
