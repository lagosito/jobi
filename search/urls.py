from django.conf.urls import url

from .views import search_view, recent_jobs_api, search_job_api, suggestions

urlpatterns = [
    url(r'^search/$', search_view, name='search_view'),
    url(r'^recent_jobs/$', recent_jobs_api, name='recent_jobs_api'),
    url(r'^search_jobs/$', search_job_api, name='job_api'),
    url(r'^suggest/$', suggestions, name='suggest'),
]
