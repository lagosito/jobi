from django.conf.urls import url

from .views import main_view, NewsletterSubscriptionView

urlpatterns = [
    url(r'^$', main_view, name='main'),
    url(r'^newsletter_add_subscription/$', NewsletterSubscriptionView.as_view(), name='newsletter_add_subscription'),
]
