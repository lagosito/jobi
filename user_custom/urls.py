from django.conf.urls import url

from user_custom.views import main_view

urlpatterns = [
    url(r'^$', main_view, name='main'),
]
