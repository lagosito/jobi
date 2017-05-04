from django.conf.urls import url

from user_custom.views import main_view, search_view

urlpatterns = [
    url(r'^$', main_view, name='main'),
    url(r'^search/$', search_view, name='search_view'),

]
