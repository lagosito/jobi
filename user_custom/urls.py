from django.conf.urls import url

from .views import main_view, NewsletterSubscriptionView, password_reset_confirm_view, activate_account_view

urlpatterns = [
    url(r'^$', main_view, name='main'),
    url(r'^newsletter_add_subscription/$', NewsletterSubscriptionView.as_view(), name='newsletter_add_subscription'),
    url(r'^password/reset/confirm/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/$', password_reset_confirm_view, name='password_reset_confirm_view'),
    url(r'^activate/(?P<uid>[\w\-]+)/(?P<token>[\w\-]+)/$', activate_account_view, name='activate_account_view'),
]
