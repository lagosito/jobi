from django.conf.urls import url

from user_custom.views import main_view, search_view, recent_jobs_api, search_job_api, NewsletterSubscriptionView

urlpatterns = [
    url(r'^$', main_view, name='main'),
    url(r'^search/$', search_view, name='search_view'),
    url(r'^recent_jobs/$', recent_jobs_api, name='recent_jobs_api'),
    
    url(r'^search_jobs/$', search_job_api, name='search_job_api'),
    url(r'^newsletter_add_subscription/$', NewsletterSubscriptionView.as_view(), name='newsletter_add_subscription'),
]
